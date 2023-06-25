"""added description to plant model

Revision ID: 0e838e9937bf
Revises: 1d58b0b8e297
Create Date: 2023-06-25 20:01:19.880771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e838e9937bf'
down_revision = '1d58b0b8e297'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=256), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('plant', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
