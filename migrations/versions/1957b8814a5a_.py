"""empty message

Revision ID: 1957b8814a5a
Revises: ded63f94ba66
Create Date: 2021-07-23 17:18:01.612000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1957b8814a5a'
down_revision = 'ded63f94ba66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reply', sa.Column('topic_id', sa.Integer(), nullable=True))
    op.add_column('reply', sa.Column('topic_type', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reply', 'topic_type')
    op.drop_column('reply', 'topic_id')
    # ### end Alembic commands ###
