from sqlalchemy.orm import Session
from . import models
from .data.languages import SUPPORTED_LANGUAGES
from .database import engine, SessionLocal
import os

def drop_tables():
    """Drop all existing tables"""
    print("Dropping existing tables...")
    models.Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully!")

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def init_languages(db: Session):
    """Initialize the database with supported languages and their initial content."""
    print("Initializing languages...")
    try:
        for lang_code, lang_data in SUPPORTED_LANGUAGES.items():
            print(f"Adding language: {lang_data['name']}")
            
            # Add language
            db_language = models.Language(
                code=lang_code,
                name=lang_data["name"],
                native_name=lang_data["native_name"],
                flag=lang_data["flag"],
                rtl=lang_data["rtl"]
            )
            db.add(db_language)
            db.flush()  # Flush to get the language ID
            
            # Add initial lessons and store them in a dictionary for reference
            lessons_by_category = {}
            if "initial_lessons" in lang_data:
                print(f"Adding {len(lang_data['initial_lessons'])} lessons for {lang_data['name']}")
                for lesson_data in lang_data["initial_lessons"]:
                    db_lesson = models.Lesson(
                        title=lesson_data["title"],
                        description=lesson_data["description"],
                        level=lesson_data["level"],
                        category=lesson_data.get("category", "Uncategorized"),  # Default category
                        content=lesson_data.get("content", {}),  # Default empty content
                        language_id=db_language.id
                    )
                    db.add(db_lesson)
                    db.flush()  # Get the lesson ID
                    
                    # Store lesson by category for phrase association
                    category = lesson_data.get("category", "Uncategorized")
                    lessons_by_category[category] = db_lesson
            
            # Add initial phrases and associate them with lessons based on category
            if "initial_phrases" in lang_data:
                print(f"Adding {len(lang_data['initial_phrases'])} phrases for {lang_data['name']}")
                for phrase_data in lang_data["initial_phrases"]:
                    # Find the appropriate lesson based on the phrase's category
                    phrase_category = phrase_data["category"]
                    associated_lesson = lessons_by_category.get(phrase_category)
                    
                    db_phrase = models.Phrase(
                        text=phrase_data["text"],
                        transliteration=phrase_data["transliteration"],
                        translation=phrase_data["translation"],
                        level=phrase_data["level"],
                        category=phrase_data["category"],
                        language_id=db_language.id,
                        lesson_id=associated_lesson.id if associated_lesson else None  # Associate with lesson if found
                    )
                    db.add(db_phrase)
            
        db.commit()
        print("Successfully initialized languages, lessons, and phrases!")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        db.rollback()
        raise

def init_db():
    """Initialize the database with tables and initial data"""
    print("Starting database initialization...")
    drop_tables()
    create_tables()
    db = SessionLocal()
    try:
        init_languages(db)
        print("Database initialization completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
