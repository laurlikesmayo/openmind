"""helloo

Revision ID: 1fcf67e55d65
Revises: 40bc1ab2517f
Create Date: 2023-03-04 13:49:54.024906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fcf67e55d65'
down_revision = '40bc1ab2517f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('replyposts', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_replies_replyto_posts', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_replies_replyposts_posts'), 'posts', ['replyposts'], ['id'])
        batch_op.drop_column('replyto')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('replies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('replyto', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_replies_replyposts_posts'), type_='foreignkey')
        batch_op.create_foreign_key('fk_replies_replyto_posts', 'posts', ['replyto'], ['id'])
        batch_op.drop_column('replyposts')

    # ### end Alembic commands ###
