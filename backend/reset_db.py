from app.init_db import drop_tables, create_tables, init_db

if __name__ == "__main__":
    print("Resetting database...")
    drop_tables()
    create_tables()
    init_db()
    print("Database reset complete!")
