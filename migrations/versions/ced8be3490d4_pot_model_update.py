"""Pot model update

Revision ID: ced8be3490d4
Revises: 01080644acb7
Create Date: 2023-08-20 14:55:54.542107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ced8be3490d4'
down_revision = '01080644acb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.alter_column('sunlight_status',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('moisture_status',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('reaction_status',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('nutrient_status',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
        batch_op.alter_column('salinity_status',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.alter_column('salinity_status',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('nutrient_status',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('reaction_status',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('moisture_status',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('sunlight_status',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
