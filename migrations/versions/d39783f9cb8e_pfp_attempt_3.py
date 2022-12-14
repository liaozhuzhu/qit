"""pfp attempt 3

Revision ID: d39783f9cb8e
Revises: 7cb5dbd3d54b
Create Date: 2022-09-14 16:26:55.714480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd39783f9cb8e'
down_revision = '7cb5dbd3d54b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about', sa.Text(length=500), nullable=True))
    op.add_column('users', sa.Column('pfp', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pfp')
    op.drop_column('users', 'about')
    # ### end Alembic commands ###
