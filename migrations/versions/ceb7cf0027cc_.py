"""empty message

Revision ID: ceb7cf0027cc
Revises: 9e30ef3cbb28
Create Date: 2021-09-18 10:43:02.004000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceb7cf0027cc'
down_revision = '9e30ef3cbb28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('comments_num', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'comments_num')
    # ### end Alembic commands ###