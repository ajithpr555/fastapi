"""add content column

Revision ID: e9623d1ea880
Revises: ef0041ad03ed
Create Date: 2025-10-06 09:05:16.848595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9623d1ea880'
down_revision: Union[str, Sequence[str], None] = 'ef0041ad03ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('posts','content')
    pass
