import subprocess
import sys
from sqlalchemy import create_engine
from alembic import command
from alembic.config import Config
from audit_log.models import Base  # 确保导入 Base
from config import DATABASE_URL  # 导入 DATABASE_URL

def run_specific_migration(revision: str) -> None:
    """Run a specific migration."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)  # Set the database URL
    command.upgrade(alembic_cfg, revision)
    print(f"Migration {revision} executed successfully.")