"""Set most atributes unnullable

Revision ID: c5fabcc75dc2
Revises: 121f8f8f18ad
Create Date: 2019-12-09 21:39:51.063455

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c5fabcc75dc2'
down_revision = '121f8f8f18ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('administrator', 'is_admin')
    op.alter_column('cemetery', 'county',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('cemetery', 'faith',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('cemetery', 'locality',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('cemetery', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('container', 'manufacturer',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('container', 'material',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('container', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('container', 'type_of_container',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('funeral', 'funeral_home_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('funeral_home', 'county',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('funeral_home', 'locality',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('funeral_home', 'name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.alter_column('funeral_home', 'phone',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('funeral_home', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('outfit', 'color',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('outfit', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('outfit', 'type_of_clothing',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('priest', 'first_name',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('priest', 'last_name',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('priest', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('priest', 'religion',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('priest', 'title',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('quarter', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('quarter', 'x_coord',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('quarter', 'y_coord',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('temple', 'county',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('temple', 'locality',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('temple', 'rank',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('temple', 'religion',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('temple', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('tombstone', 'manufacturer',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('tombstone', 'material',
               existing_type=mysql.TEXT(),
               nullable=False)
    op.alter_column('tombstone', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tombstone', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tombstone', 'material',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('tombstone', 'manufacturer',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('temple', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('temple', 'religion',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('temple', 'rank',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('temple', 'locality',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('temple', 'county',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('quarter', 'y_coord',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('quarter', 'x_coord',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('quarter', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('priest', 'title',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('priest', 'religion',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('priest', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('priest', 'last_name',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('priest', 'first_name',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('outfit', 'type_of_clothing',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('outfit', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('outfit', 'color',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('funeral_home', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('funeral_home', 'phone',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('funeral_home', 'name',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.alter_column('funeral_home', 'locality',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('funeral_home', 'county',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('funeral', 'funeral_home_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('container', 'type_of_container',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('container', 'price',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('container', 'material',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('container', 'manufacturer',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('cemetery', 'voivodeship',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('cemetery', 'locality',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('cemetery', 'faith',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('cemetery', 'county',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.add_column('administrator', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
