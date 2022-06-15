"""empty message

Revision ID: 569f55cbe26d
Revises: a6f0b6dd3490
Create Date: 2022-06-16 05:46:15.552269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '569f55cbe26d'
down_revision = 'a6f0b6dd3490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'vendors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vendor_name', sa.String(length=64), nullable=False),
        sa.Column('vendor_tin', sa.String(length=16), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('date_modified', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('vendor_name'),
        sa.UniqueConstraint('vendor_tin')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vendors')
    # ### end Alembic commands ###
