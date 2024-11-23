"""Create manual data table

Revision ID: 754fb9105b59
Revises: f3e01cc71966
Create Date: 2024-11-19 17:07:38.450950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '754fb9105b59'
down_revision: Union[str, None] = 'f3e01cc71966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None  

def upgrade() -> None:
    op.create_table(
        'manual_sleep_data',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('date', sa.String, nullable=False),
        sa.Column('nap', sa.Boolean, nullable=False),
        sa.Column('alcohol', sa.Boolean, nullable=False),
        sa.Column('food', sa.String, nullable=False),
        sa.Column('activity', sa.String, nullable=False),
        sa.Column('stretching', sa.Boolean, nullable=False),
        sa.Column('caffeine', sa.Boolean, nullable=False),
        sa.Column('sleep_quality', sa.Integer, nullable=False)
    )

def downgrade() -> None:
    op.drop_table('activity_raw')
