"""update

Revision ID: 01080644acb7
Revises: faa85060b896
Create Date: 2023-08-16 16:26:33.928023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01080644acb7'
down_revision = 'faa85060b896'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_gauge')
    with op.batch_alter_table('gauge', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=64), nullable=True))
        batch_op.alter_column('ei',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.alter_column('min_value',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('max_value',
               existing_type=sa.INTEGER(),
               nullable=False)

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

    with op.batch_alter_table('gauge', schema=None) as batch_op:
        batch_op.alter_column('max_value',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('min_value',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('ei',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
        batch_op.drop_column('name')

    op.create_table('_alembic_tmp_gauge',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('ei', sa.VARCHAR(length=64), nullable=False),
    sa.Column('eiv', sa.INTEGER(), nullable=False),
    sa.Column('min_value', sa.INTEGER(), nullable=False),
    sa.Column('max_value', sa.INTEGER(), nullable=False),
    sa.Column('description', sa.VARCHAR(length=128), nullable=True),
    sa.Column('unit', sa.VARCHAR(length=64), nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
