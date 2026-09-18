"""Seed revision paired with migration 0001_create_users."""

from sqlalchemy.engine import Connection

from app.src.core.security import get_password_hash
from app.src.domain.user.models import User


revision = "0001_create_users"
table_name = "users"


def seed(connection: Connection) -> None:
    """Create the local administrator used to explore the API."""
    connection.execute(
        User.__table__.insert().values(
            email="admin@example.com",
            hashed_password=get_password_hash("change-me"),
            is_active=True,
        )
    )
