"""empty message

Revision ID: e6853cf8e576
Revises: 9afdb9f2e39c
Create Date: 2018-12-11 18:11:50.689611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6853cf8e576'
down_revision = '9afdb9f2e39c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='social'
    )
    op.create_table('publication_social_networks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('social_network', sa.String(length=128), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['social.publications.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='social'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publication_social_networks', schema='social')
    op.drop_table('publications', schema='social')
    # ### end Alembic commands ###