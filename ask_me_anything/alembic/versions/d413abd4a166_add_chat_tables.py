"""add chat tables

Revision ID: d413abd4a166
Revises: 7530f9ec000c
Create Date: 2023-06-10 15:39:26.027525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd413abd4a166'
down_revision = '7530f9ec000c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    )
    op.create_table(
        "message",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("chat_id", sa.Integer, sa.ForeignKey("chat.id")),
        sa.Column("text", sa.String),
    )


def downgrade() -> None:
    op.drop_table("message")
    op.drop_table("chat")
