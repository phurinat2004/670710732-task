from sqlalchemy import create_engine, inspect
import importlib.util
import pathlib
import sys


def load_migration_module():
    path = pathlib.Path(__file__).parent.parent / "app" / "db" / "migrations" / "001_init.py"
    spec = importlib.util.spec_from_file_location("migration_001_init", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_migration_creates_tables():
    migration = load_migration_module()
    engine = create_engine("sqlite:///:memory:")
    migration.upgrade(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    assert {"slots", "bookings", "audit_logs"}.issubset(tables)
