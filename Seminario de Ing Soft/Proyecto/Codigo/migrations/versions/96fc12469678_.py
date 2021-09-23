"""empty message

Revision ID: 96fc12469678
Revises: a9c2322418d0
Create Date: 2021-02-09 15:33:45.661263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96fc12469678'
down_revision = 'a9c2322418d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone_number', sa.VARCHAR(length=25), nullable=True))
    # ### end Alembic commands ###