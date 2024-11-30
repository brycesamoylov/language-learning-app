import sys
from app.database import SessionLocal
from app.models import Lesson
from sqlalchemy import select

# Set stdout to handle UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def verify_lessons():
    db = SessionLocal()
    try:
        # Query all lessons in the Memory Techniques category
        stmt = select(Lesson).where(Lesson.category == "Memory Techniques")
        lessons = db.execute(stmt).scalars().all()
        
        print(f"\nFound {len(lessons)} Memory Technique lessons:")
        print("-" * 50)
        
        for lesson in lessons:
            print(f"\nLesson: {lesson.title}")
            print(f"Description: {lesson.description}")
            print(f"Level: {lesson.level}")
            print(f"Category: {lesson.category}")
            print(f"Language ID: {lesson.language_id}")
            print("\nContent Preview:")
            for key, value in lesson.content.items():
                if key == "practice_words":
                    print(f"- {key}: {len(value)} words included")
                    # Print first few words as sample
                    for i, word in enumerate(value[:3]):
                        print(f"  Sample word {i+1}: {word['word']} ({word['translation']})")
                else:
                    preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                    print(f"- {key}: {preview}")
            print("-" * 50)
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_lessons()
