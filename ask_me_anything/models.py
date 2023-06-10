from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column

from ask_me_anything.db import Base


class TextChunk(Base):
    __tablename__ = "text_chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_url = Column(String)
    text = Column(String)
    embedding = mapped_column(Vector(1536))
