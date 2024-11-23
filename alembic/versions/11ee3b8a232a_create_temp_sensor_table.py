"""Create temp sensor table

Revision ID: 11ee3b8a232a
Revises: 754fb9105b59
Create Date: 2024-11-22 23:17:36.221485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11ee3b8a232a'
down_revision: Union[str, None] = '754fb9105b59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Run the upgrade migrations."""
    op.create_table(
        'govee_temp_sensor_hourly',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sensor_id', sa.String, nullable=False),
        sa.Column('friendly_name', sa.String, nullable=False),
        sa.Column('temperature', sa.String, nullable=False),
        sa.Column('hour', sa.String, nullable=False),
        sa.Column('load_date', sa.String, nullable=False),
    )
    op.create_table(
        'govee_humidity_sensor_hourly',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sensor_id', sa.String, nullable=False),
        sa.Column('friendly_name', sa.String, nullable=False),
        sa.Column('humidity', sa.String, nullable=False),
        sa.Column('hour', sa.String, nullable=False),
        sa.Column('load_date', sa.String, nullable=False),
    )


def downgrade():
    """Run the downgrade migrations."""
    op.drop_table('govee_temp_sensor_hourly')
    op.drop_table('govee_humidity_sensor_hourly')
