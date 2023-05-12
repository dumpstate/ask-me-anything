from sqlalchemy.orm import Session

from ask_me_anything.models import TextChunk


def create_text_chunk(db: Session, text: str, embedding: list[float]) -> TextChunk:
    record = TextChunk(
        text=text,
        embedding=embedding,
    )
    db.add(record)
    return record


def get_text_chunks(db: Session, offset: int, limit: int):
    return db.query(TextChunk).offset(offset).limit(limit).all()


def find_neighbours(db: Session, v: list[float], k: int = 1):
    return db.query(TextChunk).order_by(TextChunk.embedding.l2_distance(v)).limit(k).all()