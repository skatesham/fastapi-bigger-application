from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.src.core.config import settings
from app.src.core.database import Base
from app.src.domain.buyer.models import Buyer  # noqa: F401
from app.src.domain.car.models import Car  # noqa: F401
from app.src.domain.sale.models import Sale  # noqa: F401
from app.src.domain.seller.models import Seller  # noqa: F401
from app.src.domain.stock.models import Stock  # noqa: F401
from app.src.domain.user.models import User  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importing every ORM model above ensures all tables are registered in this
# metadata object when `alembic revision --autogenerate` is run.
target_metadata = Base.metadata


def get_database_url() -> str:
    """Read the migration connection string from the same .env as the app."""
    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
