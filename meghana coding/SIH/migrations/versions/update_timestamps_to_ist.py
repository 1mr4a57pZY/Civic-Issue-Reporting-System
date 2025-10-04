"""Update timestamps to IST timezone

Revision ID: update_timestamps_to_ist
Revises: 2aa3523d58c0
Create Date: 2025-09-05 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timedelta
import pytz

# revision identifiers, used by Alembic.
revision = 'update_timestamps_to_ist'
down_revision = '2aa3523d58c0'
branch_labels = None
depends_on = None

def upgrade():
    # Update existing timestamps from UTC to IST by adding 5 hours 30 minutes
    ist_offset = timedelta(hours=5, minutes=30)
    conn = op.get_bind()

    # Update 'created_at' in 'report' table
    conn.execute(
        sa.text(
            "UPDATE report SET created_at = datetime(created_at, '+5 hours', '+30 minutes') WHERE created_at IS NOT NULL"
        )
    )
    # Update 'created_at' in 'update' table
    conn.execute(
        sa.text(
            "UPDATE \"update\" SET created_at = datetime(created_at, '+5 hours', '+30 minutes') WHERE created_at IS NOT NULL"
        )
    )
    # Update 'created_at' in 'feedback' table
    conn.execute(
        sa.text(
            "UPDATE feedback SET created_at = datetime(created_at, '+5 hours', '+30 minutes') WHERE created_at IS NOT NULL"
        )
    )

def downgrade():
    # Revert timestamps from IST to UTC by subtracting 5 hours 30 minutes
    ist_offset = timedelta(hours=5, minutes=30)
    conn = op.get_bind()

    conn.execute(
        sa.text(
            "UPDATE report SET created_at = datetime(created_at, '-5 hours', '-30 minutes') WHERE created_at IS NOT NULL"
        )
    )
    conn.execute(
        sa.text(
            "UPDATE \"update\" SET created_at = datetime(created_at, '-5 hours', '-30 minutes') WHERE created_at IS NOT NULL"
        )
    )
    conn.execute(
        sa.text(
            "UPDATE feedback SET created_at = datetime(created_at, '-5 hours', '-30 minutes') WHERE created_at IS NOT NULL"
        )
    )
