"""empty message

Revision ID: 19e36fe7d379
Revises: 83e988156958
Create Date: 2021-12-28 17:37:07.920863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19e36fe7d379'
down_revision = '83e988156958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('user_avatar', sa.String(length=256), nullable=True))
    op.add_column('comment', sa.Column('from_avatar', sa.String(length=256), nullable=True))
    op.add_column('reply', sa.Column('from_avatar', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reply', 'from_avatar')
    op.drop_column('comment', 'from_avatar')
    op.drop_column('article', 'user_avatar')
    # ### end Alembic commands ###