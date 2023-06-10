from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from ask_me_anything.db import Base


class TextChunk(Base):
    __tablename__ = "text_chunk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_url = Column(String)
    text = Column(String)
    embedding = mapped_column(Vector(1536))


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = ForeignKey(Chat.id)
    text = Column(String)
