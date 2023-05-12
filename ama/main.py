from urllib.request import urlopen

from bs4 import BeautifulSoup
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from ama.db import SessionLocal
from ama.repository import get_text_chunks
from ama.schemas import Status, TextChunk, URL


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_text(html):
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "stype"]):
        script.extract()

    text = soup.body.get_text()
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def iter_chunks(text: str):
    offset = 0

    while True:
        if offset >= len(text):
            break

        lb = max(0, offset - CHUNK_OVERLAP)
        ub = max(len(text), offset + CHUNK_SIZE + CHUNK_OVERLAP)
        yield text[lb:ub]

        offset += CHUNK_SIZE


@app.get("/api/v1/context", response_model=list[TextChunk])
def search_text_chunks(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_text_chunks(
        db=db,
        offset=offset,
        limit=limit,
    )


@app.put("/api/v1/context", response_model=Status)
def add_url_to_context(url: URL, db: Session = Depends(get_db)):
    html = urlopen(url.url).read()
    text = get_text(html)

    print("\n\n".join(iter_chunks(text)))

    # TODO for each chunk, compute and persist embeddings
    return Status(success=True)
