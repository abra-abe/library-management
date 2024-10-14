from logging.config import fileConfig
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool

from alembic import context
from app.db import engine  # Adjust this import based on your project structure

# This is the Alembic Config object, it provides access to the .ini file settings
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Metadata for Alembic's `autogenerate`
target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine  # Use the engine from app.db

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether we're running in "offline" or "online" mode and run accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
