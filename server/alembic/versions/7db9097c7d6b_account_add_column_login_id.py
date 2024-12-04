"""account add column login_id

Revision ID: 7db9097c7d6b
Revises: 70799a1a2321
Create Date: 2024-12-04 18:52:44.175818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7db9097c7d6b"
down_revision: Union[str, None] = "70799a1a2321"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "account", sa.Column("login_id", sa.VARCHAR(length=30), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("account", "login_id")
