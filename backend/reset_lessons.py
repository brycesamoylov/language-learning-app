from app.database import SessionLocal, add_memory_technique_lessons, add_greetings_lesson
from app.models import Lesson
from sqlalchemy import delete

def reset_lessons():
    db = SessionLocal()
    try:
        # Delete existing greetings lesson
        stmt = delete(Lesson).where(Lesson.lesson_type == "greetings")
        db.execute(stmt)
        db.commit()
        print("Deleted existing greetings lesson")

        # Add new greetings lesson
        greetings_lesson = add_greetings_lesson(db, 1)  # 1 is the ID for Greek language
        print("Added new greetings lesson")
        
        # Delete existing memory technique lessons
        stmt = delete(Lesson).where(Lesson.category == "Memory Techniques")
        db.execute(stmt)
        db.commit()
        print("Deleted existing memory technique lessons")
        
        # Add new memory technique lessons
        lessons = add_memory_technique_lessons(db, 1)  # 1 is the ID for Greek language
        print(f"Added {len(lessons)} new memory technique lessons")
        
    finally:
        db.close()

if __name__ == "__main__":
    reset_lessons()
