"""Add otp_created_at column to User model

Revision ID: add_otp_created_at_column
Revises: 
Create Date: 2024-06-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_otp_created_at_column'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('otp_created_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('user', 'otp_created_at')
