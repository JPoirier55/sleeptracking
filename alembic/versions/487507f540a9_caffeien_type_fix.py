"""Caffeien type fix

Revision ID: 487507f540a9
Revises: 11ee3b8a232a
Create Date: 2024-11-23 11:51:55.947583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '487507f540a9'
down_revision: Union[str, None] = '11ee3b8a232a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Change `age` column type from Integer to String
    op.alter_column(
        'manual_sleep_data',                  # Table name
        'caffeine',                    # Column name
        type_=sa.String(),        # New type
        existing_type=sa.Boolean(), # Current type
        nullable=False             # Specify if column should allow NULL
    )

def downgrade():
    # Revert `age` column type back to Integer
    op.alter_column(
        'manual_sleep_data',
        'caffeine',
        type_=sa.Boolean(),
        existing_type=sa.String(),
        nullable=False
    )
