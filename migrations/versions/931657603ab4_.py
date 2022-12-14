"""empty message

Revision ID: 931657603ab4
Revises: 7442dbae48ab
Create Date: 2022-07-26 22:19:57.423038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '931657603ab4'
down_revision = '7442dbae48ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
