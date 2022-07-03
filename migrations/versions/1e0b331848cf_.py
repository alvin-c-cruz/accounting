"""empty message

Revision ID: 1e0b331848cf
Revises: 9922187b21d7
Create Date: 2022-07-03 18:00:37.697204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e0b331848cf'
down_revision = '9922187b21d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('record_date', sa.DateTime(), nullable=False),
    sa.Column('bank_date', sa.DateTime(), nullable=True),
    sa.Column('receipt_number', sa.String(length=32), nullable=False),
    sa.Column('invoice_number', sa.String(length=32), nullable=False),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('receipt_number')
    )
    op.create_table('receipts_entry',
    sa.Column('entry_id', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('debit', sa.Float(), nullable=True),
    sa.Column('credit', sa.Float(), nullable=True),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('entry_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receipts_entry')
    op.drop_table('receipts')
    # ### end Alembic commands ###