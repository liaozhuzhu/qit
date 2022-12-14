"""update

Revision ID: 95384a5964d6
Revises: efd6b3ce9ea7
Create Date: 2022-09-16 01:47:43.465602

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '95384a5964d6'
down_revision = 'efd6b3ce9ea7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('commentor_id', sa.Integer(), nullable=True))
    op.drop_constraint('comments_ibfk_3', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['commentor_id'], ['id'])
    op.drop_column('comments', 'commentor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('commentor', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_ibfk_3', 'comments', 'users', ['commentor'], ['id'])
    op.drop_column('comments', 'commentor_id')
    # ### end Alembic commands ###
