"""create post_ideas table

Revision ID: 20260210_0001
Revises:
Create Date: 2026-02-10 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260210_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post_ideas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(length=30), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("caption", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("hashtags", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_post_ideas_id", "post_ideas", ["id"], unique=False)
    op.create_index("ix_post_ideas_platform", "post_ideas", ["platform"], unique=False)
    op.create_index("ix_post_ideas_status", "post_ideas", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_post_ideas_status", table_name="post_ideas")
    op.drop_index("ix_post_ideas_platform", table_name="post_ideas")
    op.drop_index("ix_post_ideas_id", table_name="post_ideas")
    op.drop_table("post_ideas")
