"""account update column token

Revision ID: 70799a1a2321
Revises: 675398e14411
Create Date: 2024-12-04 16:37:37.852713

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70799a1a2321"
down_revision: Union[str, None] = "675398e14411"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 임시 테이블 생성
    op.create_table(
        "new_account",
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
        sa.Column("broker_type", sa.CHAR(length=10), nullable=False),
        sa.Column("token", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.drop_index("ix_account_number", table_name="account")
    op.create_index(op.f("ix_account_number"), "new_account", ["number"], unique=False)

    # 2. 데이터 이전
    op.execute(
        """
        INSERT INTO new_account
        SELECT id, created_at, updated_at, name, number, product_code, app_key, secret_key, url_base, broker_type, null
        FROM account
        """
    )

    # 3. 기존 테이블 삭제
    op.drop_table("account")

    # 4. 임시 테이블 이름 변경
    op.rename_table("new_account", "account")


def downgrade() -> None:
    # 1. 임시 테이블 생성

    op.create_table(
        "new_account",
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
        sa.Column("broker_type", sa.CHAR(length=10), nullable=False),
        sa.Column("token", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        if_not_exists=True,
    )
    op.drop_index("ix_account_number", table_name="account")
    op.create_index(op.f("ix_account_number"), "new_account", ["number"], unique=False)

    # 2. 데이터 이전
    op.execute(
        """
        INSERT INTO new_account
        SELECT id, created_at, updated_at, name, number, product_code, app_key, secret_key, url_base, broker_type, null
        FROM account
        """
    )

    # 3. 기존 테이블 삭제
    op.drop_table("account")

    # 4. 임시 테이블 이름 변경
    op.rename_table("new_account", "account")
