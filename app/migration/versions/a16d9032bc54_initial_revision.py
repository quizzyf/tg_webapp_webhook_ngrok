"""Initial revision

Revision ID: a16d9032bc54
Revises: c4ec7c75ac33
Create Date: 2024-12-15 19:30:22.310705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a16d9032bc54'
down_revision: Union[str, None] = 'c4ec7c75ac33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('basket', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'basket')
    # ### end Alembic commands ###
