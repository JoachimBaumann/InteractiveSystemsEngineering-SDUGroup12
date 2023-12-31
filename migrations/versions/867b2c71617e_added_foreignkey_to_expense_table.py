"""added foreignKey to Expense table

Revision ID: 867b2c71617e
Revises: 6eb61bceb50a
Create Date: 2023-11-05 15:40:17.544313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867b2c71617e'
down_revision = '6eb61bceb50a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_expense_category', 'category', ['category_id'], ['id'])
        # If you're replacing 'category' with 'category_id', uncomment the next line.
        # batch_op.drop_column('category')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.VARCHAR(length=80), nullable=True))  # nullable=True because the original might have had data
        batch_op.drop_constraint('fk_expense_category', type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
