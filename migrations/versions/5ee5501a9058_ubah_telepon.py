"""ubah-telepon

Revision ID: 5ee5501a9058
Revises: ca2b397a9120
Create Date: 2023-10-22 07:29:13.066703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5ee5501a9058'
down_revision = 'ca2b397a9120'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mahasiswa', 'no_telepon',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('mahasiswa', 'no_telepon',
               existing_type=sa.String(length=50),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    # ### end Alembic commands ###
