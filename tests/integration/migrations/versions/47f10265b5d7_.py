"""empty message

Revision ID: 47f10265b5d7
Revises:
Create Date: 2022-08-30 14:18:25.483981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "47f10265b5d7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "integration_test", sa.Column("message", sa.String(), nullable=False), sa.PrimaryKeyConstraint("message")
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("integration_test")
    # ### end Alembic commands ###
