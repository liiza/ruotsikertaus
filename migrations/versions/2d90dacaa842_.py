"""empty message

Revision ID: 2d90dacaa842
Revises: 3b38504d2100
Create Date: 2014-10-09 10:56:41.168832

"""

# revision identifiers, used by Alembic.
revision = '2d90dacaa842'
down_revision = '3b38504d2100'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'expression',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('finnish', sa.Unicode(length=200), nullable=False),
        sa.Column('swedish', sa.Unicode(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table(
    'expression')
