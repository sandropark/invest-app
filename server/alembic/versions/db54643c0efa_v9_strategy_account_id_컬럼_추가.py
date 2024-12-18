"""V9_Strategy account_id 컬럼 추가

Revision ID: db54643c0efa
Revises: 3dba3d8de1cf
Create Date: 2024-12-18 17:59:08.541452

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "db54643c0efa"
down_revision: Union[str, None] = "3dba3d8de1cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.add_column(
            sa.Column("account_id", sa.INTEGER(), nullable=False, server_default="1")
        )
        batch_op.create_foreign_key(
            "fk_strategy_account", "account", ["account_id"], ["id"]
        )


def downgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.drop_constraint("fk_strategy_account", type_="foreignkey")
        batch_op.drop_column("account_id")
