"""empty message

Revision ID: 5d8f254b0b26
Revises: 6dd93a8ec9b3
Create Date: 2023-10-02 00:38:14.849998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d8f254b0b26'
down_revision: Union[str, None] = '6dd93a8ec9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
