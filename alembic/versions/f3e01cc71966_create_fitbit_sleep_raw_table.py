"""Create fitbit sleep raw table

Revision ID: f3e01cc71966
Revises: c60707e1ec0f
Create Date: 2024-11-19 09:37:15.865586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3e01cc71966'
down_revision: Union[str, None] = 'c60707e1ec0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Run the upgrade migrations."""
    op.create_table(
        'sleep_raw',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('json_blob', sa.String, nullable=False),
        sa.Column('load_date', sa.String, nullable=False),
    )


def downgrade():
    """Run the downgrade migrations."""
    op.drop_table('sleep_raw')
