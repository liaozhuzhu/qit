"""liker

Revision ID: 4da489e31620
Revises: 749080ccbed4
Create Date: 2022-09-14 22:51:20.869529

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4da489e31620'
down_revision = '749080ccbed4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('liker', sa.Integer(), nullable=True))
    op.drop_constraint('likes_ibfk_2', 'likes', type_='foreignkey')
    op.create_foreign_key(None, 'likes', 'users', ['liker'], ['id'])
    op.drop_column('likes', 'poster_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('poster_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.create_foreign_key('likes_ibfk_2', 'likes', 'users', ['poster_id'], ['id'])
    op.drop_column('likes', 'liker')
    # ### end Alembic commands ###