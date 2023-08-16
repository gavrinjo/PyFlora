"""sensor update

Revision ID: faa85060b896
Revises: 67025b4d4b58
Create Date: 2023-08-16 14:12:48.513480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faa85060b896'
down_revision = '67025b4d4b58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor_measurements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sunlight', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('temperature', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('reaction', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('nutrient', sa.Integer(), nullable=True))
        batch_op.alter_column('moisture',
               existing_type=sa.NUMERIC(precision=3, scale=2),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.drop_column('ph_range')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sensor_measurements', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ph_range', sa.INTEGER(), nullable=True))
        batch_op.alter_column('moisture',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=3, scale=2),
               existing_nullable=True)
        batch_op.drop_column('nutrient')
        batch_op.drop_column('reaction')
        batch_op.drop_column('temperature')
        batch_op.drop_column('sunlight')

    # ### end Alembic commands ###
