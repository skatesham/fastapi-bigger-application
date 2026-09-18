"""Run seed revisions after their corresponding Alembic migrations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from importlib import import_module
from typing import Callable

from sqlalchemy import Column, DateTime, MetaData, String, Table, select
from sqlalchemy.engine import Connection

from app.src.core.database import engine
from app.src.domain.buyer.models import Buyer  # noqa: F401
from app.src.domain.car.models import Car  # noqa: F401
from app.src.domain.sale.models import Sale  # noqa: F401
from app.src.domain.seller.models import Seller  # noqa: F401
from app.src.domain.stock.models import Stock  # noqa: F401
from app.src.domain.user.models import User  # noqa: F401


@dataclass(frozen=True)
class SeedRevision:
    revision: str
    module: str


# Keep this order aligned with db/migration/versions.
SEED_REVISIONS = (
    SeedRevision("0001_create_users", "0001_users"),
    SeedRevision("0002_create_buyers", "0002_buyers"),
    SeedRevision("0003_create_sellers", "0003_sellers"),
    SeedRevision("0004_create_cars", "0004_cars"),
    SeedRevision("0005_create_stocks", "0005_stocks"),
    SeedRevision("0006_create_sales", "0006_sales"),
)

metadata = MetaData()
seed_history = Table(
    "seed_history",
    metadata,
    Column("revision", String(64), primary_key=True),
    Column("applied_at", DateTime(timezone=True), nullable=False),
)


def get_current_migration_revision(connection: Connection) -> str:
    """Return the current revision from Alembic's version table."""
    try:
        return connection.exec_driver_sql(
            "SELECT version_num FROM alembic_version"
        ).scalar_one()
    except Exception as error:
        raise RuntimeError(
            "No Alembic revision was found. Run `alembic upgrade head` first."
        ) from error


def ready_seed_revisions(current_revision: str) -> tuple[SeedRevision, ...]:
    """Return seeds whose table migrations have already been applied.

    Migrations are currently a linear history. A new seed must be added after
    its migration in this sequence, using the same migration revision id.
    """
    for index, seed_revision in enumerate(SEED_REVISIONS):
        if seed_revision.revision == current_revision:
            return SEED_REVISIONS[: index + 1]
    raise RuntimeError(
        f"Migration revision {current_revision!r} is not registered for seeds."
    )


def load_seed(module_name: str) -> Callable[[Connection], None]:
    module = import_module(f"db.seed.versions.{module_name}")
    return module.seed


def run() -> None:
    """Apply each pending seed once and record it in ``seed_history``."""
    with engine.begin() as connection:
        metadata.create_all(connection)
        current_revision = get_current_migration_revision(connection)
        applied_revisions = set(
            connection.execute(select(seed_history.c.revision)).scalars()
        )

        for seed_revision in ready_seed_revisions(current_revision):
            if seed_revision.revision in applied_revisions:
                continue

            load_seed(seed_revision.module)(connection)
            connection.execute(
                seed_history.insert().values(
                    revision=seed_revision.revision,
                    applied_at=datetime.now(timezone.utc),
                )
            )
            print(f"Applied seed {seed_revision.revision}")
