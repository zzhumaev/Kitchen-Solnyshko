"""rbac + prices + daily_metrics

Revision ID: 5c87c082f7ff
Revises: 
Create Date: 2025-09-12 04:45:46.289637
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "5c87c082f7ff"
down_revision = None  # в этой ветке начинаем историю миграций с нуля
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- RBAC: users/roles/user_roles ---------------------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("tg_user_id", sa.BigInteger(), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_unique_constraint("uq_users_tg_user_id", "users", ["tg_user_id"])

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
    )
    op.create_unique_constraint("uq_roles_code", "roles", ["code"])

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("granted_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    # --- История цен ---------------------------------------------------------
    op.create_table(
        "product_prices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price", sa.Numeric(14, 2), nullable=False),
        sa.Column("start_at", sa.Date(), nullable=False),
        sa.Column("end_at", sa.Date(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_product_prices_product_start", "product_prices", ["product_id", "start_at"], unique=False)
    op.create_check_constraint(
        "ck_product_prices_date_range",
        "product_prices",
        "(end_at IS NULL) OR (end_at > start_at)",
    )

    # --- Ежедневные показатели (дети/сотрудники) ----------------------------
    op.create_table(
        "daily_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("location_id", sa.Integer(), sa.ForeignKey("locations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("children_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("staff_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_unique_constraint("uq_daily_metrics_date_location", "daily_metrics", ["date", "location_id"])


def downgrade() -> None:
    # удаляем в обратном порядке зависимостей
    op.drop_table("daily_metrics")
    op.drop_index("ix_product_prices_product_start", table_name="product_prices")
    op.drop_table("product_prices")
    op.drop_table("user_roles")
    op.drop_constraint("uq_roles_code", "roles", type_="unique")
    op.drop_table("roles")
    op.drop_constraint("uq_users_tg_user_id", "users", type_="unique")
    op.drop_table("users")

