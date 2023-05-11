from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from ama.db import SessionLocal
from ama.repository import get_text_chunks
from ama.schemas import TextChunk


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/text_chunk", response_model=list[TextChunk])
def search_text_chunks(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_text_chunks(
        db=db,
        offset=offset,
        limit=limit,
    )
