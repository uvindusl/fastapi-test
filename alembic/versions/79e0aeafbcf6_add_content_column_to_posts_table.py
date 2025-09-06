"""add content column to posts table

Revision ID: 79e0aeafbcf6
Revises: 73efa4f44032
Create Date: 2025-09-07 00:17:15.392206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79e0aeafbcf6'
down_revision: Union[str, Sequence[str], None] = '73efa4f44032'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
