"""V7_토큰  컬럼 수정

Revision ID: 601ddf04234d
Revises: 000ebf5f332c
Create Date: 2024-12-10 17:41:29.621148

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = "601ddf04234d"
down_revision: Union[str, None] = "000ebf5f332c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("account", "token")
    op.add_column("account", sa.Column("token", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("account", "token")
    op.add_column("account", sa.Column("token", sqlite.VARCHAR(100), nullable=True))
