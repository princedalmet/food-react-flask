"""Adjust phone_number column in User table

Revision ID: 89d4178862c7
Revises: 6cbaab426af6
Create Date: 2024-10-24 12:09:07.321148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89d4178862c7'
down_revision = '6cbaab426af6'
branch_labels = None
depends_on = None


def upgrade():
    # Set a default value for phone_number where it's NULL
    op.execute("UPDATE users SET phone_number = '000-000-0000' WHERE phone_number IS NULL")
    
    # Alter the 'phone_number' column to be non-nullable
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone_number', existing_type=sa.VARCHAR(length=15), nullable=False)


def downgrade():
    # Revert the 'phone_number' column to allow NULL
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone_number', existing_type=sa.VARCHAR(length=15), nullable=True)

def upgrade():
    op.alter_column('users', 'phone_number', nullable=True)
