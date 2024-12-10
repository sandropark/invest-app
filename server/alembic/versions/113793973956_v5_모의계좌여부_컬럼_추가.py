"""V5_모의계좌여부 컬럼 추가

Revision ID: 113793973956
Revises: 60c12596bf9a
Create Date: 2024-12-10 09:15:34.540603

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = "113793973956"
down_revision: Union[str, None] = "60c12596bf9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "account",
        sa.Column(
            "is_virtual", sa.BOOLEAN(), server_default=sa.text("0"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_column("account", "is_virtual")
