"""add foreign key to posts table

Revision ID: a1604e9bd2fa
Revises: 819d2aebb29d
Create Date: 2025-10-06 09:24:39.834755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1604e9bd2fa'
down_revision: Union[str, Sequence[str], None] = '819d2aebb29d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fkey',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constratint('post_users_fkey',table_name='posts')
    op.drop_column('posts','owner_id',)
    pass
