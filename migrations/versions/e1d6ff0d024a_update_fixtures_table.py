"""Update fixtures table

Revision ID: e1d6ff0d024a
Revises: 91afa6beedb3
Create Date: 2020-06-21 11:14:10.789805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1d6ff0d024a'
down_revision = '91afa6beedb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fixtures', sa.Column('confirmed', sa.Integer(), nullable=True))
    op.add_column('fixtures', sa.Column('declined', sa.Integer(), nullable=True))
    op.add_column('fixtures', sa.Column('opponent', sa.String(), nullable=True))
    op.add_column('fixtures', sa.Column('requester', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fixtures', 'requester')
    op.drop_column('fixtures', 'opponent')
    op.drop_column('fixtures', 'declined')
    op.drop_column('fixtures', 'confirmed')
    # ### end Alembic commands ###