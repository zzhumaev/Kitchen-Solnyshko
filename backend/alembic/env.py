import os, sys
from pathlib import Path
from logging.config import fileConfig
from app.db.base import Base
from app.db import models  # noqa

from alembic import context
from sqlalchemy import engine_from_config, pool

# === СДЕЛАТЬ /app видимым для Python ===
BASE_DIR = Path(__file__).resolve().parents[1]  # /app
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# === Импорт Base.metadata из твоего проекта ===
# Попробуем несколько мест — оставь то, где реально лежит Base
c
config = context.config

# URL берём из переменной окружения (DATABASE_URL приходит из .env)
db_url = os.getenv("DATABASE_URL", "")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Логи Alembic из alembic.ini
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
