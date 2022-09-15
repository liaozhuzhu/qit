"""removed likes

Revision ID: 7f44c269fae8
Revises: 4da489e31620
Create Date: 2022-09-15 15:09:40.926420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7f44c269fae8'
down_revision = '4da489e31620'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('liker', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['liker'], ['users.id'], name='likes_ibfk_2'),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='likes_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###