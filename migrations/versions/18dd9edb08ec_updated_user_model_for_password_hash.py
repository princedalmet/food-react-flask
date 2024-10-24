"""Updated User model for password_hash

Revision ID: 18dd9edb08ec
Revises: b990b312efb9
Create Date: 2024-10-24 17:54:39.010249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18dd9edb08ec'
down_revision = 'b990b312efb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)

    # ### end Alembic commands ###
