"""make email unique

Revision ID: df859fbbc812
Revises: 1543ca5173bd
Create Date: 2025-03-07 08:04:37.590838

"""

from typing import Sequence, Union

from alembic import op


revision: str = "df859fbbc812"
down_revision: Union[str, None] = "1543ca5173bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
