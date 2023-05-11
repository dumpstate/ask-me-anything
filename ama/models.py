from sqlalchemy import Column, Integer, String

from ama.db import Base


class TextChunk(Base):
    __tablename__ = "text_chunk"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
