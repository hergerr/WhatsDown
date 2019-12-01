"""Cleaned authorisation code

Revision ID: ee1555d09cdf
Revises: 7c4a5c87d104
Create Date: 2019-11-05 20:22:10.415275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee1555d09cdf'
down_revision = '7c4a5c87d104'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('funeral_home', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funeral_home', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###