"""Readded price for funeral home

Revision ID: 121f8f8f18ad
Revises: 97b2f4e48fb5
Create Date: 2019-11-29 20:47:56.193998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '121f8f8f18ad'
down_revision = '97b2f4e48fb5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funeral_home', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('funeral_home', 'price')
    # ### end Alembic commands ###
