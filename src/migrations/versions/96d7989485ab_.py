"""empty message

Revision ID: 96d7989485ab
Revises: 
Create Date: 2018-11-23 16:44:03.262939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96d7989485ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facebook_auth',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=2048), nullable=True),
    sa.Column('code_created', sa.DateTime(), nullable=True),
    sa.Column('short_lived_access_token', sa.String(length=128), nullable=True),
    sa.Column('short_lived_access_token_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='social'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('facebook_auth', schema='social')
    # ### end Alembic commands ###
