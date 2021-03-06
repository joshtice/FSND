"""empty message

Revision ID: 2f92ea86c43c
Revises: f354d5942756
Create Date: 2019-09-17 21:53:52.273661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f92ea86c43c'
down_revision = 'f354d5942756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre_artists',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.PrimaryKeyConstraint('genre_id', 'artist_id')
    )
    op.create_table('genre_venues',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('genre_id', 'venue_id')
    )
    op.add_column('city', sa.Column('name', sa.String(length=120), nullable=True))
    op.drop_column('city', 'city')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('city', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('city', 'name')
    op.drop_table('genre_venues')
    op.drop_table('genre_artists')
    op.drop_table('genre')
    # ### end Alembic commands ###
