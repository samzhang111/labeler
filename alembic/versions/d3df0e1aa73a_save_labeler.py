"""Save labeler

Revision ID: d3df0e1aa73a
Revises:
Create Date: 2017-01-13 22:17:15.598442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3df0e1aa73a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('labels') as batch_op:
        batch_op.add_column(sa.Column('labeler', sa.String()))
        batch_op.add_column(sa.Column('labeler_ip', sa.String()))

def downgrade():
    with op.batch_alter_table('labels') as batch_op:
        batch_op.drop_column('labeler')
        batch_op.drop_column('labeler_ip')
