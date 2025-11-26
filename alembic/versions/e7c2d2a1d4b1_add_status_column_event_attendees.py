"""add status column to event_attendees

Revision ID: e7c2d2a1d4b1
Revises: b3da49f46516
Create Date: 2025-11-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e7c2d2a1d4b1"
down_revision: Union[str, Sequence[str], None] = "b3da49f46516"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add status column with default."""
    op.add_column(
        "event_attendees",
        sa.Column("status", sa.String(), server_default="Maybe", nullable=False),
    )
    # Drop the server default so future inserts rely on application-level defaults.
    op.alter_column(
        "event_attendees",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Remove status column."""
    op.drop_column("event_attendees", "status")


