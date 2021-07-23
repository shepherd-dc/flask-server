"""empty message

Revision ID: 9a71280acb8b
Revises: f8578b3c6404
Create Date: 2021-07-21 10:06:44.789000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a71280acb8b'
down_revision = 'f8578b3c6404'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('user_name', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'user_name')
    # ### end Alembic commands ###
