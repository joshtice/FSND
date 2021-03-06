"""empty message

Revision ID: 6ae0e6b3a735
Revises: 0ad64fddb6ab
Create Date: 2019-09-15 19:00:42.201674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ae0e6b3a735'
down_revision = '0ad64fddb6ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('artist', sa.Column('city_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'artist', 'city', ['city_id'], ['id'])
    op.drop_column('artist', 'state')
    op.drop_column('artist', 'city')
    op.add_column('venue', sa.Column('city_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'venue', 'city', ['city_id'], ['id'])
    op.drop_column('venue', 'state')
    op.drop_column('venue', 'city')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('venue', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'venue', type_='foreignkey')
    op.drop_column('venue', 'city_id')
    op.add_column('artist', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'artist', type_='foreignkey')
    op.drop_column('artist', 'city_id')
    op.drop_table('city')
    # ### end Alembic commands ###
