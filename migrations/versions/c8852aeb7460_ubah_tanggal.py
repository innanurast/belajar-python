"""ubah tanggal

Revision ID: c8852aeb7460
Revises: cea20acd0f51
Create Date: 2023-10-22 16:08:28.221233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c8852aeb7460'
down_revision = 'cea20acd0f51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('keanggotaan', 'tanggal_masuk',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('keanggotaan', 'tanggal_masuk',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###
