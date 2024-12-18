"""V8_Account env 컬럼 제거

Revision ID: 3dba3d8de1cf
Revises: 601ddf04234d
Create Date: 2024-12-18 17:39:00.176057

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3dba3d8de1cf"
down_revision: Union[str, None] = "601ddf04234d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("strategy", "env")


def downgrade() -> None:
    op.add_column("strategy", sa.Column("env", sa.CHAR(length=1), nullable=False))
