from sqlalchemy import MetaData, create_engine, inspect
import importlib


def upgrade(engine):
    """Create initial tables: slots, bookings, audit_logs

    This migration is intentionally simple and intended for use in tests
    with SQLite in-memory as well as PostgreSQL in real deployment.
    """
    # Import ORM models and create tables.
    # Prefer package import, but fall back to file-based import when running tests
    try:
        models = importlib.import_module("backend.app.db.models")
    except Exception:
        # Resolve file path relative to this migration file
        import pathlib
        import importlib.util
        migration_dir = pathlib.Path(__file__).resolve().parent
        models_path = migration_dir.parent / "models.py"
        spec = importlib.util.spec_from_file_location("backend.app.db.models", str(models_path))
        models = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(models)

    Base = getattr(models, "Base")
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # Quick verification runner for the migration (uses SQLite in-memory)
    engine = create_engine("sqlite:///:memory:")
    upgrade(engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    print("Created tables:", tables)
    expected = {"slots", "bookings", "audit_logs"}
    missing = expected - tables
    if missing:
        print("MISSING TABLES:", missing)
        raise SystemExit(2)
    print("Migration verification: OK")
