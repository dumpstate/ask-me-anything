from pydantic import BaseModel


class TextChunk(BaseModel):
    id: int
    text: str
