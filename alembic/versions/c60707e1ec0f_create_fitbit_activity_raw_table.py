"""Create fitbit activity raw table

Revision ID: c60707e1ec0f
Revises: 
Create Date: 2024-11-19 08:18:16.831557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c60707e1ec0f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Run the upgrade migrations."""
    op.create_table(
        'activity_raw',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('json_blob', sa.String, nullable=False),
        sa.Column('load_date', sa.String, nullable=False),
    )


def downgrade():
    """Run the downgrade migrations."""
    op.drop_table('activity_raw')
