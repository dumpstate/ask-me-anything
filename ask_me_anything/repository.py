from sqlalchemy.orm import Session

from ask_me_anything.models import Chat, TextChunk


def create_text_chunk(db: Session, source_url: str, text: str, embedding: list[float]) -> TextChunk:
    record = TextChunk(
        source_url=source_url,
        text=text,
        embedding=embedding,
    )
    db.add(record)
    return record


def get_text_chunks(db: Session, offset: int, limit: int):
    return db.query(TextChunk).offset(offset).limit(limit).all()


def find_neighbours(db: Session, v: list[float], k: int = 1):
    return db.query(TextChunk).order_by(TextChunk.embedding.l2_distance(v)).limit(k).all()


def create_chat(db: Session) -> Chat:
    record = Chat()
    db.add(record)
    return record


def get_chat(db: Session, chat_id: int) -> Chat:
    return db.query(Chat).filter(Chat.id == chat_id).one()
