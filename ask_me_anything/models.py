from enum import Enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum as EnumCol, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ask_me_anything.db import Base


class TextChunk(Base):
    __tablename__ = "text_chunk"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_url: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536))


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Author(Enum):
    HUMAN = "human"
    BOT = "bot"


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author: Mapped[Author] = mapped_column(EnumCol(Author), nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
