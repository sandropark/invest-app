"""Init

Revision ID: 675398e14411
Revises: 
Create Date: 2024-12-04 12:31:52.759703

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "675398e14411"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "strategy",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("invest_rate", sa.Float(), nullable=False),
        sa.Column("env", sa.CHAR(length=1), nullable=False, server_default="R"),
        sa.Column("stocks", sa.JSON(), nullable=True),
        sa.Column("interval", sa.JSON(), nullable=False),
        sa.Column("last_run", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_strategy_name"), "strategy", ["name"], unique=False)

    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("number", sa.String(length=10), nullable=False),
        sa.Column("product_code", sa.CHAR(length=2), nullable=False),
        sa.Column("app_key", sa.String(length=50), nullable=False),
        sa.Column("secret_key", sa.String(length=100), nullable=False),
        sa.Column("url_base", sa.String(length=100), nullable=False),
        sa.Column("token", sa.String(length=200), nullable=True),
        sa.Column("broker_type", sa.CHAR(length=10), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_account_number"), "account", ["number"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_account_number"), table_name="account")
    op.drop_table("account")
    op.drop_index(op.f("ix_strategy_name"), table_name="strategy")
    op.drop_table("strategy")
