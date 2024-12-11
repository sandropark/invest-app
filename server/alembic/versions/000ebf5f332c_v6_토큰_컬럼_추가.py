"""V6_토튼 컬럼 추가

Revision ID: 000ebf5f332c
Revises: 113793973956
Create Date: 2024-12-10 09:22:14.172338

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = "000ebf5f332c"
down_revision: Union[str, None] = "113793973956"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("account", sa.Column("token", sa.VARCHAR(length=100), nullable=True))


def downgrade() -> None:
    op.drop_column("account", "token")
