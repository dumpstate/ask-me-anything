"""create text_chunk table

Revision ID: 7530f9ec000c
Revises: 
Create Date: 2023-05-11 23:01:44.393666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7530f9ec000c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "text_chunk",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("text", sa.String)
    )


def downgrade() -> None:
    op.drop_table("text_chunk")
