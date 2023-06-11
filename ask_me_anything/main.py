from typing import Annotated

import openai
from fastapi import Depends, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from langchain.chains import LLMChain
from langchain.document_loaders import WebBaseLoader
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session

from ask_me_anything.config import Config
from ask_me_anything.db import SessionLocal
from ask_me_anything.models import Author, TextChunk
from ask_me_anything.repository import (
    create_chat,
    create_message,
    create_text_chunk,
    find_neighbours,
    get_chat,
    get_messages,
    get_text_chunks,
)
from ask_me_anything.schemas import Answer, Chat, Question, Status, TextChunk, URL


OPENAI_EMBEDDING_ENGINE = "text-embedding-ada-002"


app = FastAPI()
config = Config.load()
templates = Jinja2Templates(directory="ask_me_anything/templates")
llm = OpenAI(openai_api_key=config.openai_api_key)
question_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
        You're a helpful assistant.

        Given the context provided in ``` quotes:

        ```
        {context}
        ```

        {question}
    """.strip(),
)
question_chain = LLMChain(llm=llm, prompt=question_prompt)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_embedding(text: str):
    return openai.Embedding.create(
        input=[text.replace("\n", " ")],
        engine=OPENAI_EMBEDDING_ENGINE,
    )["data"][0]["embedding"]


@app.get("/api/v1/context", response_model=list[TextChunk])
def search_text_chunks(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_text_chunks(
        db=db,
        offset=offset,
        limit=limit,
    )


@app.put("/api/v1/context", response_model=Status)
def add_url_to_context(url: URL, db: Session = Depends(get_db)):
    loader = WebBaseLoader(url.url)
    documents = loader.load_and_split()

    with db.begin():
        for document in documents:
            embedding = get_embedding(document.page_content)
            create_text_chunk(db, url.url, document.page_content, embedding)

    db.commit()

    return Status(success=True)


@app.post("/api/v1/question", response_model=Answer)
def ask_a_question(question: Question, db: Session = Depends(get_db)):
    embedding = get_embedding(question.question)
    ns = find_neighbours(db, embedding, 3)
    context = "\n\n".join(n.text for n in ns)

    print(context)

    answer = question_chain.run(
        question=question.question,
        context=context,
    )

    return Answer(answer=answer)


@app.post("/api/v1/chat", response_model=Chat)
def start_chat(db: Session = Depends(get_db)):
    with db.begin():
        chat = create_chat(db)

    db.commit()

    return Chat(id=chat.id)


@app.get("/")
def ask_anything(request: Request):
    return templates.TemplateResponse("ask_anything.html", {"request": request})


@app.get("/chat/{chat_id}")
def chat(request: Request, chat_id: int, db: Session = Depends(get_db)):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat": get_chat(db, chat_id),
        "messages": get_messages(db, chat_id),
    })


@app.post("/chat/{chat_id}")
def submit_message(
    request: Request,
    chat_id: int,
    message: Annotated[str, Form()],
    db: Session = Depends(get_db),
):
    chat = get_chat(db, chat_id)
    create_message(db, chat_id, Author.HUMAN, message)

    db.commit()

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat": chat,
        "messages": get_messages(db, chat_id),
    })
