"""empty message

Revision ID: a4d2e52be5b2
Revises: 887b09149371
Create Date: 2019-01-13 22:48:06.794151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4d2e52be5b2'
down_revision = '887b09149371'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publication_tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['social.publications.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='social'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publication_tags', schema='social')
    # ### end Alembic commands ###
