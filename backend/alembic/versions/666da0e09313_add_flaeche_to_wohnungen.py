"""add flaeche to wohnungen

Revision ID: 666da0e09313
Revises: a6130fe8f439
Create Date: 2026-07-13 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '666da0e09313'
down_revision: Union[str, Sequence[str], None] = 'a6130fe8f439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('wohnungen', sa.Column('flaeche', sa.Float(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('wohnungen', 'flaeche')
