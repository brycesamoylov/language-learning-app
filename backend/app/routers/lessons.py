from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
import logging
import traceback
import sys
from sqlalchemy import text
from datetime import datetime
from ..data.vocabulary import popularGreekWords
from ..data.alphabet import greek_alphabet

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

def generate_lesson_content(lesson_type: str, words: list, level: str = "A1"):
    """Generate lesson content based on the lesson type"""
    logger.debug(f"Generating content for lesson type: {lesson_type} with {len(words)} words")
    
    # Convert words and explanations into a single string
    words_string = ";".join([
        f"{word['word']}:{word.get('explanation', 'No explanation available')}"
        for word in words
    ])

    content = {
        "introduction": "",
        "description": "",
        "activities": [],
        "words": words,  # Store the original words list
        "example_situations": []
    }
    
    if lesson_type == "alphabet":
        content["introduction"] = "Learn the Greek alphabet and pronunciation"
        content["description"] = "Master the building blocks of the Greek language by learning the alphabet and its sounds"
        content["activities"] = [
            "Listen and repeat each letter sound",
            "Practice writing the letters",
            "Match letters with their sounds",
            "Identify letters in common words"
        ]
        
    elif lesson_type == "greetings":
        content["introduction"] = "Essential Greek greetings and farewells"
        content["description"] = "Learn common Greek expressions for greeting people and saying goodbye"
        content["activities"] = [
            "Practice pronunciation of each greeting",
            "Role-play greeting scenarios",
            "Match greetings with appropriate situations",
            "Complete dialogue exercises"
        ]
        content["example_situations"] = [
            "Meeting someone for the first time",
            "Greeting a friend in the morning",
            "Saying goodbye after a meeting",
            "Wishing someone a good night"
        ]
        
    elif lesson_type == "spaced_repetition":
        content["introduction"] = "Spaced Repetition Practice"
        content["description"] = "Review and reinforce vocabulary using scientifically-proven spaced repetition techniques"
        content["activities"] = [
            "Review previously learned words",
            "Practice recall with flashcards",
            "Complete fill-in-the-blank exercises",
            "Test your memory with timed challenges"
        ]
        
    elif lesson_type == "mnemonics":
        content["introduction"] = "Mnemonic devices are memory aids that help you remember words through associations."
        content["description"] = "Mnemonics are memory aids that help link new information to existing knowledge through vivid imagery, stories, or patterns. Each word below includes a mnemonic device to help you remember its meaning and pronunciation."
        content["activities"] = [
            "Create memorable associations",
            "Practice visualization techniques",
            "Connect words with similar sounds",
            "Build memory palaces"
        ]
        content["example"] = 'For the Greek word "νερό" (water), you might imagine a "narrow" stream of water to remember the pronunciation.'
        content["benefits"] = "Makes learning more engaging and can significantly improve recall by creating strong mental connections."
        
    elif lesson_type == "contextual":
        content["introduction"] = "Learn Greek in Context"
        content["description"] = "Master Greek vocabulary by learning words in their natural context"
        content["activities"] = [
            "Study words in context",
            "Practice with real-life scenarios",
            "Complete contextual exercises",
            "Build sentences with new words"
        ]
        
    elif lesson_type == "visual":
        content["introduction"] = "Visual Learning Techniques"
        content["description"] = "Learn Greek vocabulary through visual associations and memory techniques"
        content["activities"] = [
            "Create visual associations",
            "Practice with image-based flashcards",
            "Draw and sketch word meanings",
            "Build visual memory palaces"
        ]
    
    logger.debug(f"Generated content with {len(content['words'])} words")
    return content

@router.get("/{language_code}", response_model=List[schemas.Lesson])
def get_lessons_by_language(response: Response, language_code: str, db: Session = Depends(get_db)):
    """Get all lessons for a specific language"""
    try:
        logger.debug("=== Starting get_lessons_by_language ===")
        logger.debug(f"Parameters: language_code={language_code}")
        
        # Debug: Check if we can execute a simple query
        try:
            test_query = db.execute(text("SELECT 1"))
            logger.debug("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Database connection error")

        # Debug: Check if languages table exists and has data
        try:
            languages_count = db.execute(text("SELECT COUNT(*) FROM languages")).scalar()
            logger.debug(f"Number of languages in database: {languages_count}")
        except Exception as e:
            logger.error(f"Error checking languages table: {str(e)}")
            raise HTTPException(status_code=500, detail="Error accessing languages table")
        
        # First verify the language exists
        logger.debug("Querying database for language")
        try:
            language = db.query(models.Language).filter(models.Language.code == language_code).first()
            if language:
                logger.debug(f"Found language: ID={language.id}, name={language.name}")
            else:
                logger.debug(f"No language found with code: {language_code}")
        except Exception as e:
            logger.error(f"Error querying language: {str(e)}")
            raise HTTPException(status_code=500, detail="Error querying language")
        
        if not language:
            logger.error(f"Language not found: {language_code}")
            raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
        
        # Get all lessons for this language
        logger.debug(f"Querying lessons for language_id: {language.id}")
        try:
            lessons = db.query(models.Lesson).filter(models.Lesson.language_id == language.id).all()
            logger.debug(f"Found {len(lessons)} lessons")
            
            # Debug: Print each lesson's details
            for lesson in lessons:
                logger.debug(f"Lesson ID: {lesson.id}")
                logger.debug(f"Title: {lesson.title}")
                logger.debug(f"Level: {lesson.level}")
                logger.debug(f"Category: {lesson.category}")
        except Exception as e:
            logger.error(f"Error querying lessons: {str(e)}")
            raise HTTPException(status_code=500, detail="Error querying lessons")
        
        # Add CORS headers to the response
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        
        logger.debug("=== Completed get_lessons_by_language successfully ===")
        return lessons
    except HTTPException as he:
        logger.error(f"HTTP Exception in get_lessons_by_language: {str(he)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_lessons_by_language: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{language_code}/{lesson_id}", response_model=schemas.LessonDetail)
def get_lesson_detail(response: Response, language_code: str, lesson_id: int, db: Session = Depends(get_db)):
    """Get detailed information for a specific lesson"""
    try:
        logger.debug("=== Starting get_lesson_detail ===")
        logger.debug(f"Parameters: language_code={language_code}, lesson_id={lesson_id}")
        
        # First verify the language exists
        language = db.query(models.Language).filter(models.Language.code == language_code).first()
        if not language:
            raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
        
        # Get the specific lesson
        lesson = db.query(models.Lesson).filter(
            models.Lesson.language_id == language.id,
            models.Lesson.id == lesson_id
        ).first()
        
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson with ID {lesson_id} not found")
        
        logger.debug(f"Found lesson: {lesson.title}")
        logger.debug(f"Lesson content type: {type(lesson.content)}")
        logger.debug(f"Lesson content: {lesson.content}")
        
        # Ensure content has the required structure
        content = lesson.content
        if isinstance(content, str):
            # If content is a string, try to parse it
            try:
                import json
                content = json.loads(content)
            except json.JSONDecodeError:
                logger.error("Failed to parse lesson content as JSON")
                content = {
                    "introduction": "",
                    "description": "",
                    "activities": [],
                    "words": [],
                    "example_situations": []
                }
        
        # Ensure activities is a list
        if "activities" not in content or not isinstance(content["activities"], list):
            content["activities"] = []
            
        # Convert practice_words to words if needed
        if "practice_words" in content and not content.get("words"):
            content["words"] = content["practice_words"]
            
        # Ensure words is a list and preserve mnemonic/context fields
        if "words" not in content or not isinstance(content["words"], list):
            # Try to split words string if it exists
            if isinstance(content.get("words"), str) and content["words"]:
                content["words"] = [
                    {"word": w.split(":")[0], "explanation": w.split(":")[1] if ":" in w else ""}
                    for w in content["words"].split(";")
                    if w.strip()
                ]
            else:
                content["words"] = []
        else:
            # Ensure each word has the required fields
            processed_words = []
            for word in content["words"]:
                if isinstance(word, dict):
                    # Preserve all existing fields and ensure required ones exist
                    processed_word = {
                        "word": word.get("word", ""),
                        "translation": word.get("translation", ""),
                        "transliteration": word.get("transliteration", ""),
                    }
                    # Preserve mnemonic if it exists
                    if "mnemonic" in word:
                        processed_word["mnemonic"] = word["mnemonic"]
                    # Preserve context if it exists
                    if "context" in word:
                        processed_word["context"] = word["context"]
                    processed_words.append(processed_word)
                else:
                    # Handle simple string words
                    processed_words.append({"word": str(word), "translation": "", "transliteration": ""})
            content["words"] = processed_words
        
        logger.debug(f"Processed content: {content}")
        
        # Return the lesson detail with the content from the database
        lesson_detail = schemas.LessonDetail(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            level=lesson.level,
            category=lesson.category,
            content=content,  # Use the processed content
            language_id=lesson.language_id,
            lesson_type=lesson.lesson_type
        )
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return lesson_detail
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in get_lesson_detail: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{language_code}/initialize", response_model=List[schemas.Lesson])
def initialize_lessons(response: Response, language_code: str, db: Session = Depends(get_db)):
    """Initialize lessons for a language"""
    try:
        logger.debug("=== Starting initialize_lessons ===")
        logger.debug(f"Parameters: language_code={language_code}")
        
        # Verify the language exists
        language = db.query(models.Language).filter(models.Language.code == language_code).first()
        if not language:
            raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
        
        # Define lesson types and their configurations
        lesson_configs = [
            {
                "title": "Greek Alphabet",
                "description": "Learn the Greek alphabet and pronunciation",
                "level": "A1",
                "category": "Fundamentals",
                "lesson_type": "alphabet"
            },
            {
                "title": "Basic Greetings",
                "description": "Essential Greek greetings and farewells",
                "level": "A1",
                "category": "Conversation",
                "lesson_type": "greetings"
            },
            {
                "title": "Spaced Repetition Practice",
                "description": "Review and reinforce vocabulary using scientifically-proven spaced repetition techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "spaced_repetition"
            },
            {
                "title": "Mnemonic Devices for Greek",
                "description": "Learn to create memorable associations for Greek vocabulary using mnemonic devices",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "mnemonics"
            },
            {
                "title": "Contextual Learning",
                "description": "Master Greek vocabulary by learning words in real-life situations",
                "level": "A1",
                "category": "Vocabulary",
                "lesson_type": "contextual"
            },
            {
                "title": "Visual Association Learning",
                "description": "Master Greek vocabulary through powerful visual associations and memory techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "visual"
            }
        ]
        
        # Create lessons
        created_lessons = []
        for config in lesson_configs:
            # Check if lesson already exists
            existing_lesson = db.query(models.Lesson).filter(
                models.Lesson.language_id == language.id,
                models.Lesson.title == config["title"]
            ).first()
            
            if not existing_lesson:
                # Select words based on lesson type
                if config["lesson_type"] == "alphabet":
                    words = greek_alphabet
                elif config["lesson_type"] == "greetings":
                    words = [w for w in popularGreekWords[25:50] if w["word"] in [
                        "γεια", "καλημέρα", "καληνύχτα", "ευχαριστώ", "παρακαλώ", "συγγνώμη"
                    ]]
                elif config["lesson_type"] == "spaced_repetition":
                    words = popularGreekWords[:25]
                elif config["lesson_type"] == "mnemonics":
                    words = popularGreekWords[25:50]
                    logger.debug(f"Mnemonic words selected: {words}")  # Log selected words
                elif config["lesson_type"] == "contextual":
                    words = popularGreekWords[50:75]
                elif config["lesson_type"] == "visual":
                    words = popularGreekWords[75:100]
                else:
                    words = []
                
                # Create new lesson
                lesson = models.Lesson(
                    title=config["title"],
                    description=config["description"],
                    level=config["level"],
                    category=config["category"],
                    lesson_type=config["lesson_type"],
                    language_id=language.id,
                    content=generate_lesson_content(config["lesson_type"], words, config["level"])
                )
                db.add(lesson)
                db.commit()
                db.refresh(lesson)
                created_lessons.append(lesson)
                logger.debug(f"Created lesson: {lesson.title} with {len(words)} words")
            else:
                logger.debug(f"Lesson already exists: {config['title']}")
                created_lessons.append(existing_lesson)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        
        logger.debug("=== Completed initialize_lessons successfully ===")
        return created_lessons
        
    except HTTPException as he:
        logger.error(f"HTTP Exception in initialize_lessons: {str(he)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in initialize_lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{language_code}/reinitialize", response_model=List[schemas.Lesson])
def reinitialize_lessons(response: Response, language_code: str, db: Session = Depends(get_db)):
    """Reinitialize lessons for a language"""
    try:
        # First verify the language exists
        language = db.query(models.Language).filter(models.Language.code == language_code).first()
        if not language:
            raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
            
        # Delete existing lessons for this language
        db.query(models.Lesson).filter(models.Lesson.language_id == language.id).delete()
        db.commit()
        
        # Initialize new lessons
        from ..database import init_db
        init_db(db, language.id)
        
        # Get all lessons for this language
        lessons = db.query(models.Lesson).filter(models.Lesson.language_id == language.id).all()
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return lessons
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in reinitialize_lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{language_code}/initialize", response_model=List[schemas.Lesson])
def initialize_lessons(response: Response, language_code: str, db: Session = Depends(get_db)):
    """Initialize lessons for a language"""
    try:
        logger.debug("=== Starting initialize_lessons ===")
        logger.debug(f"Parameters: language_code={language_code}")
        
        # Verify the language exists
        language = db.query(models.Language).filter(models.Language.code == language_code).first()
        if not language:
            raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
        
        # Define lesson types and their configurations
        lesson_configs = [
            {
                "title": "Greek Alphabet",
                "description": "Learn the Greek alphabet and pronunciation",
                "level": "A1",
                "category": "Fundamentals",
                "lesson_type": "alphabet"
            },
            {
                "title": "Basic Greetings",
                "description": "Essential Greek greetings and farewells",
                "level": "A1",
                "category": "Conversation",
                "lesson_type": "greetings"
            },
            {
                "title": "Spaced Repetition Practice",
                "description": "Review and reinforce vocabulary using scientifically-proven spaced repetition techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "spaced_repetition"
            },
            {
                "title": "Mnemonic Devices for Greek",
                "description": "Learn to create memorable associations for Greek vocabulary using mnemonic devices",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "mnemonics"
            },
            {
                "title": "Contextual Learning",
                "description": "Master Greek vocabulary by learning words in real-life situations",
                "level": "A1",
                "category": "Vocabulary",
                "lesson_type": "contextual"
            },
            {
                "title": "Visual Association Learning",
                "description": "Master Greek vocabulary through powerful visual associations and memory techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "visual"
            }
        ]
        
        # Create lessons
        created_lessons = []
        for config in lesson_configs:
            # Check if lesson already exists
            existing_lesson = db.query(models.Lesson).filter(
                models.Lesson.language_id == language.id,
                models.Lesson.title == config["title"]
            ).first()
            
            if not existing_lesson:
                # Select words based on lesson type
                if config["lesson_type"] == "alphabet":
                    words = greek_alphabet
                elif config["lesson_type"] == "greetings":
                    words = [w for w in popularGreekWords[25:50] if w["word"] in [
                        "γεια", "καλημέρα", "καληνύχτα", "ευχαριστώ", "παρακαλώ", "συγγνώμη"
                    ]]
                elif config["lesson_type"] == "spaced_repetition":
                    words = popularGreekWords[:25]
                elif config["lesson_type"] == "mnemonics":
                    words = popularGreekWords[25:50]
                    logger.debug(f"Mnemonic words selected: {words}")  # Log selected words
                elif config["lesson_type"] == "contextual":
                    words = popularGreekWords[50:75]
                elif config["lesson_type"] == "visual":
                    words = popularGreekWords[75:100]
                else:
                    words = []
                
                # Create new lesson
                lesson = models.Lesson(
                    title=config["title"],
                    description=config["description"],
                    level=config["level"],
                    category=config["category"],
                    lesson_type=config["lesson_type"],
                    language_id=language.id,
                    content=generate_lesson_content(config["lesson_type"], words, config["level"])
                )
                db.add(lesson)
                db.commit()
                db.refresh(lesson)
                created_lessons.append(lesson)
                logger.debug(f"Created lesson: {lesson.title} with {len(words)} words")
            else:
                logger.debug(f"Lesson already exists: {config['title']}")
                created_lessons.append(existing_lesson)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, Accept"
        
        logger.debug("=== Completed initialize_lessons successfully ===")
        return created_lessons
        
    except HTTPException as he:
        logger.error(f"HTTP Exception in initialize_lessons: {str(he)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in initialize_lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/initialize-greek", response_model=List[schemas.Lesson])
def initialize_greek_lessons(response: Response, db: Session = Depends(get_db)):
    """Initialize Greek language and lessons"""
    try:
        logger.debug("=== Starting initialize_greek_lessons ===")
        
        # First check if Greek language exists
        greek = db.query(models.Language).filter(models.Language.code == "el").first()
        if not greek:
            # Create Greek language
            greek = models.Language(
                code="el",
                name="Greek",
                native_name="Ελληνικά",
                flag="🇬🇷",
                rtl=False
            )
            db.add(greek)
            db.commit()
            db.refresh(greek)
            logger.debug("Created Greek language entry")
        
        # Define lesson types and their configurations
        lesson_configs = [
            {
                "title": "Greek Alphabet",
                "description": "Learn the Greek alphabet and pronunciation",
                "level": "A1",
                "category": "Fundamentals",
                "lesson_type": "alphabet"
            },
            {
                "title": "Basic Greetings",
                "description": "Essential Greek greetings and farewells",
                "level": "A1",
                "category": "Conversation",
                "lesson_type": "greetings"
            },
            {
                "title": "Spaced Repetition Practice",
                "description": "Review and reinforce vocabulary using scientifically-proven spaced repetition techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "spaced_repetition"
            },
            {
                "title": "Mnemonic Devices for Greek",
                "description": "Learn to create memorable associations for Greek vocabulary using mnemonic devices",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "mnemonics"
            },
            {
                "title": "Contextual Learning",
                "description": "Master Greek vocabulary by learning words in real-life situations",
                "level": "A1",
                "category": "Vocabulary",
                "lesson_type": "contextual"
            },
            {
                "title": "Visual Association Learning",
                "description": "Master Greek vocabulary through powerful visual associations and memory techniques",
                "level": "A1",
                "category": "Memory Techniques",
                "lesson_type": "visual"
            }
        ]
        
        # Create lessons
        created_lessons = []
        for config in lesson_configs:
            # Check if lesson already exists
            existing_lesson = db.query(models.Lesson).filter(
                models.Lesson.language_id == greek.id,
                models.Lesson.title == config["title"]
            ).first()
            
            if not existing_lesson:
                # Select words based on lesson type
                if config["lesson_type"] == "alphabet":
                    words = greek_alphabet
                elif config["lesson_type"] == "greetings":
                    words = [w for w in popularGreekWords[25:50] if w["word"] in [
                        "γεια", "καλημέρα", "καληνύχτα", "ευχαριστώ", "παρακαλώ", "συγγνώμη"
                    ]]
                elif config["lesson_type"] == "spaced_repetition":
                    words = popularGreekWords[:25]
                elif config["lesson_type"] == "mnemonics":
                    words = popularGreekWords[25:50]
                    logger.debug(f"Mnemonic words selected: {words}")  # Log selected words
                elif config["lesson_type"] == "contextual":
                    words = popularGreekWords[50:75]
                elif config["lesson_type"] == "visual":
                    words = popularGreekWords[75:100]
                else:
                    words = []
                
                # Generate content for the lesson
                content = generate_lesson_content(config["lesson_type"], words, config["level"])
                
                # Create new lesson
                lesson = models.Lesson(
                    title=config["title"],
                    description=config["description"],
                    level=config["level"],
                    category=config["category"],
                    lesson_type=config["lesson_type"],
                    content=content,
                    language_id=greek.id
                )
                db.add(lesson)
                created_lessons.append(lesson)
                logger.debug(f"Created lesson: {lesson.title}")
        
        if created_lessons:
            db.commit()
            for lesson in created_lessons:
                db.refresh(lesson)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        
        # Return all lessons for the language
        all_lessons = db.query(models.Lesson).filter(models.Lesson.language_id == greek.id).all()
        return all_lessons
        
    except Exception as e:
        logger.error(f"Error in initialize_greek_lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup-duplicates", response_model=List[schemas.Lesson])
def cleanup_duplicate_lessons(response: Response, db: Session = Depends(get_db)):
    """Remove duplicate lessons while keeping only the specified ones with their content"""
    try:
        # Get Greek language
        greek = db.query(models.Language).filter(models.Language.code == "el").first()
        if not greek:
            raise HTTPException(status_code=404, detail="Greek language not found")

        # List of lessons to keep with their exact titles
        lessons_to_keep = {
            "Greek Alphabet": "alphabet",
            "Basic Greetings": "greetings",
            "Spaced Repetition Practice": "spaced_repetition",
            "Mnemonic Devices for Greek": "mnemonics",
            "Contextual Learning": "contextual",
            "Visual Association Learning": "visual"
        }

        # Get all lessons for Greek
        all_lessons = db.query(models.Lesson).filter(models.Lesson.language_id == greek.id).all()
        
        # Keep track of which lessons we want to keep
        kept_lessons = []
        seen_titles = set()

        # First pass: find lessons with exact titles and keep them
        for lesson in all_lessons:
            if lesson.title in lessons_to_keep and lesson.title not in seen_titles:
                kept_lessons.append(lesson)
                seen_titles.add(lesson.title)
                logger.debug(f"Keeping lesson: {lesson.title}")
            else:
                # Delete lesson if it's not in our keep list
                logger.debug(f"Deleting lesson: {lesson.title}")
                db.delete(lesson)

        db.commit()

        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"

        # Return the lessons we kept
        return kept_lessons

    except Exception as e:
        logger.error(f"Error in cleanup_duplicate_lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
