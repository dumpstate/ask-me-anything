from sqlalchemy.orm import Session

from ama.models import TextChunk


def get_text_chunks(db: Session, offset: int, limit: int):
    return db.query(TextChunk).offset(offset).limit(limit).all()
