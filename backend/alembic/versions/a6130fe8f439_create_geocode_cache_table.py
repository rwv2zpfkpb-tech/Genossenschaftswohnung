"""create geocode_cache table

Revision ID: a6130fe8f439
Revises: ce15e2b24646
Create Date: 2026-07-13 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6130fe8f439'
down_revision: Union[str, Sequence[str], None] = 'ce15e2b24646'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('geocode_cache',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adresse', sa.String(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('geocoded_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_geocode_cache_adresse'), 'geocode_cache', ['adresse'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_geocode_cache_adresse'), table_name='geocode_cache')
    op.drop_table('geocode_cache')
