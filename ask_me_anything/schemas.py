from pydantic import BaseModel


class URL(BaseModel):
    url: str


class Status(BaseModel):
    success: bool


class TextChunk(BaseModel):
    id: int
    text: str


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str
