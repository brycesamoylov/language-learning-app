from app.database import SessionLocal
from app.models import Language
from sqlalchemy import select

def add_greek_language():
    db = SessionLocal()
    try:
        # Check if Greek language already exists
        stmt = select(Language).where(Language.code == "el")
        existing = db.execute(stmt).scalar_one_or_none()
        
        if not existing:
            # Add Greek language
            greek = Language(
                code="el",  # ISO 639-1 code for Greek
                name="Greek",
                native_name="Ελληνικά",
                flag="🇬🇷",
                rtl=False
            )
            db.add(greek)
            db.commit()
            print("Added Greek language to database")
        else:
            print("Greek language already exists in database")
            
    finally:
        db.close()

if __name__ == "__main__":
    add_greek_language()
