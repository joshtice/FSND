"""empty message

Revision ID: 28fdf0547c8e
Revises: f62757c9e225
Create Date: 2019-10-02 21:29:24.664025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28fdf0547c8e'
down_revision = 'f62757c9e225'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'artist', ['name'])
    op.create_unique_constraint('unique_city_state', 'city', ['city', 'state'])
    op.create_unique_constraint(None, 'genre', ['name'])
    op.create_unique_constraint('unique_start_time', 'show', ['artist_id', 'start_time'])
    op.create_unique_constraint(None, 'venue', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venue', type_='unique')
    op.drop_constraint('unique_start_time', 'show', type_='unique')
    op.drop_constraint(None, 'genre', type_='unique')
    op.drop_constraint('unique_city_state', 'city', type_='unique')
    op.drop_constraint(None, 'artist', type_='unique')
    # ### end Alembic commands ###
