"""create text_chunk table

Revision ID: 7530f9ec000c
Revises: 
Create Date: 2023-05-11 23:01:44.393666

"""
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision = "7530f9ec000c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "text_chunk",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("source_url", String),
        Column("text", String),
        Column("embedding", Vector(1536))
    )


def downgrade() -> None:
    op.drop_table("text_chunk")
