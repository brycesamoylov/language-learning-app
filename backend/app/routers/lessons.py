from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
import time
from .. import models, schemas
from ..database import get_db, add_memory_technique_lessons
import logging
import traceback
import sys
from sqlalchemy import text
from datetime import datetime
from ..data.vocabulary import popularGreekWords
from ..data.alphabet import greek_alphabet
from ..data.greetings import greek_greetings
from ..data.mnemonics import mnemonics_data

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Visual hints dictionary at module level
visual_hints = {
    "φεγγάρι": "Picture a bright, silvery moon hanging in the night sky, casting a gentle glow",
    "αστέρι": "Imagine a twinkling star shining brightly against the dark sky",
    "ουρανός": "Visualize a vast, blue sky stretching endlessly above you",
    "θάλασσα": "Picture waves of crystal-clear blue water gently lapping at a sandy shore",
    "βουνό": "Imagine a majestic mountain peak covered in snow, reaching up to the clouds",
    "δέντρο": "Picture a tall, strong tree with branches swaying in the breeze",
    "λουλούδι": "Visualize a colorful flower blooming in a sunny garden",
    "ζώο": "Picture various animals moving and playing in their natural habitats",
    "σκύλος": "Imagine a friendly dog wagging its tail and playing fetch",
    "γάτα": "Picture a graceful cat stretching lazily in a patch of sunlight",
    "πουλί": "Visualize a small bird soaring through the air with outstretched wings",
    "ψάρι": "Imagine a colorful fish swimming smoothly through clear water",
    "χρώμα": "Picture an artist's palette filled with vibrant colors",
    "κόκκινο": "Visualize a bright red rose in full bloom",
    "μπλε": "Picture the deep blue color of the Mediterranean Sea",
    "πράσινο": "Imagine the fresh green color of spring leaves",
    "κίτρινο": "Picture a bright yellow sun shining in a clear sky",
    "άσπρο": "Visualize pure white snow covering a winter landscape",
    "μαύρο": "Picture the deep black color of a starless night sky",
    "γκρι": "Imagine soft grey clouds floating in the sky",
    "καφέ": "Picture rich brown earth in a garden",
    "ροζ": "Visualize delicate pink cherry blossoms in spring",
    "μωβ": "Picture fields of purple lavender swaying in the breeze",
    "πορτοκαλί": "Imagine a juicy orange fruit or a beautiful sunset"
}

# Detailed visualization text for each word in the Visual Association Learning lesson
visual_visualization_text = {
    "φεγγάρι": "Close your eyes and picture a full moon on a clear night. Notice how its silvery light bathes everything in a soft, ethereal glow. Feel the peaceful atmosphere it creates. This is 'fengari' - the moon that watches over the Greek islands.",
    
    "αστέρι": "Imagine looking up at the night sky and seeing one particularly bright star that catches your eye. Watch it twinkle and dance against the dark backdrop. This brilliant point of light is 'asteri' - a star that guides travelers.",
    
    "ουρανός": "Stand outside and look up at a vast expanse of brilliant blue sky. Feel its endless depth stretching to the horizon. This infinite canvas above you is 'ouranos' - the sky that holds all of nature's wonders.",
    
    "θάλασσα": "Picture yourself standing on a Greek beach, watching crystal-clear turquoise waters gently lap at the shore. Feel the salty breeze and hear the rhythmic waves. This is 'thalassa' - the Mediterranean sea that embraces Greece.",
    
    "βουνό": "Visualize a majestic mountain peak rising up through the clouds, its snow-capped summit gleaming in the sunlight. Feel its solid presence and timeless strength. This is 'vouno' - a mountain standing proud against the sky.",
    
    "δέντρο": "Imagine an ancient olive tree, its gnarled trunk telling stories of centuries past, its silver-green leaves dancing in the breeze. Feel its deep roots connecting to the earth. This is 'dentro' - a tree that provides shelter and sustenance.",
    
    "λουλούδι": "Picture a bright red poppy swaying gently in a spring breeze, its delicate petals catching the sunlight. Smell its subtle fragrance. This is 'louloudi' - a flower bringing color to the Greek landscape.",
    
    "ζώο": "Visualize a variety of animals - a playful dolphin leaping through waves, a mountain goat scaling steep cliffs, a soaring eagle. Feel their energy and freedom. These are 'zoo' - the animals that share our world.",
    
    "σκύλος": "Imagine a friendly dog bounding toward you, tail wagging with pure joy, eager to play and share affection. Feel its unconditional love. This is 'skilos' - a dog that becomes part of the family.",
    
    "γάτα": "Picture a graceful cat stretching lazily in a patch of warm sunlight, its contentment evident in its soft purring. Watch it move with elegant precision. This is 'gata' - a cat enjoying its peaceful moment.",
    
    "πουλί": "Visualize a small bird soaring through the air, its wings spread wide as it rides the wind currents. Hear its melodious song echoing through the trees. This is 'pouli' - a bird expressing the freedom of flight.",
    
    "ψάρι": "Imagine a colorful fish gliding effortlessly through clear blue waters, its scales shimmering like jewels in the sunlight. Watch its fluid movements. This is 'psari' - a fish in its underwater paradise.",
    
    "χρώμα": "Picture an artist's palette filled with vibrant pigments - deep blues, bright yellows, rich reds. See how they blend and dance together. These are 'hroma' - the colors that paint our world.",
    
    "κόκκινο": "Visualize the deepest, richest red you've ever seen - like a perfect rose in full bloom or the sun setting over the sea. Feel its warmth and passion. This is 'kokkino' - the color red in all its intensity.",
    
    "μπλε": "Imagine the perfect blue of the Mediterranean Sea on a sunny day, where the water meets the sky in an endless azure expanse. Feel its cool, refreshing presence. This is 'ble' - the color blue in its purest form.",
    
    "πράσινο": "Picture the fresh green of new spring leaves, bright and full of life, promising growth and renewal. Feel the vitality it represents. This is 'prasino' - the color green in nature's palette.",
    
    "κίτρινο": "Visualize a field of sunflowers turning their bright yellow faces to follow the sun across the sky. Feel their warmth and cheerfulness. This is 'kitrino' - the color yellow radiating joy.",
    
    "άσπρο": "Imagine freshly fallen snow covering everything in pure, pristine white, creating a peaceful blanket of silence. Feel its clean, crisp presence. This is 'aspro' - the color white in its most perfect form.",
    
    "μαύρο": "Picture a starless night sky, deep and mysterious, holding secrets in its velvety darkness. Feel its depth and power. This is 'mavro' - the color black in its most profound state.",
    
    "γκρι": "Visualize soft grey clouds drifting across the sky, neither dark nor light but perfectly balanced between the two. Feel their gentle, calming presence. This is 'gri' - the color grey in nature.",
    
    "καφέ": "Picture rich, fertile soil in a garden, ready to nurture new life, or the warm brown of coffee beans promising morning energy. This is 'kafe' - the color brown in its most natural state.",
    
    "ροζ": "Imagine delicate pink cherry blossoms floating on a spring breeze, their soft color bringing gentle beauty to the world. Feel their sweet, romantic presence. This is 'roz' - the color pink in its most charming form.",
    
    "μωβ": "Visualize a field of lavender swaying in the breeze, their purple flowers creating waves of color and releasing their soothing fragrance. This is 'mov' - the color purple in nature's garden.",
    
    "πορτοκαλί": "Picture a Mediterranean sunset painting the sky in brilliant orange, or a ripe orange fruit bursting with sweet juice. Feel its vibrant energy. This is 'portokali' - the color orange in its most vivid form."
}

class RateLimitError(Exception):
    pass

def handle_rate_limit():
    """Handle rate limit by implementing exponential backoff"""
    wait_time = 5  # Start with 5 seconds
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            yield
            break  # If successful, break out of the loop
        except Exception as e:
            if "rate limit exceeded" in str(e).lower():
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff
                else:
                    raise RateLimitError("Rate limit exceeded. Please try again in a few minutes.")
            else:
                raise e

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

def generate_mnemonic_hint(word, translation, transliteration):
    # Simple example of generating a mnemonic hint
    # This can be replaced with a more sophisticated algorithm
    return f"Associate {word} with {translation} by thinking of a {transliteration} sound"

def generate_lesson_content(lesson_type: str, words: List[dict], level: str = "A1") -> dict:
    """Generate lesson content based on the lesson type"""
    logger.debug(f"Generating content for lesson type: {lesson_type} with {len(words)} words")
    
    content = {
        "introduction": "",
        "description": "",
        "activities": [],
        "words": [],  # Initialize empty words list
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
        content["letters"] = []  # Initialize empty letters list
        
        # Add alphabet data
        for letter in greek_alphabet:
            content["letters"].append({
                "letter": letter["letter"],
                "name": letter["name"],
                "transliteration": letter["transliteration"],
                "pronunciation": letter["pronunciation"],
                "example": letter["example_word"]
            })
    
    elif lesson_type == "greetings":
        content["introduction"] = "Essential Greek greetings and farewells"
        content["description"] = "Learn common Greek expressions for greeting people and saying goodbye in various situations"
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
        content["words"] = []
        
        # Add greetings data
        for word in greek_greetings:
            content["words"].append({
                "word": word["word"],
                "translation": word["translation"],
                "transliteration": word["transliteration"],
                "context": word["context"],
                "category": word["category"]
            })
    
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
        
        # Create a lookup dictionary for mnemonics
        mnemonics_lookup = {m["word"]: m["mnemonic"] for m in mnemonics_data}
        
        # Add words from the passed words list with mnemonics
        content["words"] = []
        for word in words:
            # Use predefined mnemonic if available, otherwise generate a simple one
            mnemonic = mnemonics_lookup.get(word["word"]) or f'Associate "{word["transliteration"]}" with {word["translation"]}'
            
            content["words"].append({
                "word": word["word"],
                "translation": word["translation"],
                "transliteration": word["transliteration"],
                "mnemonic": mnemonic
            })
    
    elif lesson_type == "contextual":
        content["introduction"] = "Learn Greek in Context"
        content["description"] = "Master Greek vocabulary by learning words in their natural context"
        content["activities"] = [
            "Study words in context",
            "Practice with real-life scenarios",
            "Complete contextual exercises",
            "Build sentences with new words"
        ]
        
        # Ensure words are added to the content
        content["words"] = [
            {
                "word": word["word"],
                "translation": word["translation"],
                "transliteration": word["transliteration"],
                "context": word.get("context", "No context available")
            }
            for word in words
        ]
    
    elif lesson_type == "visual":
        content["introduction"] = "Visual Learning Techniques"
        content["description"] = """Master Greek vocabulary through powerful visual associations. Each word is paired with a detailed 
        visualization to help create strong mental connections. Take a moment to close your eyes and imagine each scene vividly."""
        content["activities"] = [
            "Create detailed mental images for each word",
            "Practice visualization exercises",
            "Draw simple sketches to reinforce connections",
            "Build a visual memory palace"
        ]
        content["visualization_tips"] = [
            "Take a few seconds to fully imagine each scene",
            "Add colors, sounds, and movement to your mental images",
            "Connect the images to personal experiences",
            "Practice recalling the images regularly"
        ]
        
        # Process words for visual learning
        content["words"] = []  # Initialize words list
        for word in words:
            word_data = {
                "word": word["word"],
                "translation": word["translation"],
                "transliteration": word["transliteration"],
                "visual_hint": visual_hints.get(word["word"], ""),
                "visualization_text": visual_visualization_text.get(word["word"], "")
            }
            content["words"].append(word_data)
    
    elif lesson_type == "spaced_repetition":
        content["introduction"] = "Spaced Repetition Practice"
        content["description"] = "Review and reinforce vocabulary using scientifically-proven spaced repetition techniques"
        content["activities"] = [
            "Review previously learned words",
            "Practice recall with flashcards",
            "Complete fill-in-the-blank exercises",
            "Test your memory with timed challenges"
        ]
        
        # Add words from the passed words list
        content["words"] = []
        for word in words:
            content["words"].append({
                "word": word["word"],
                "translation": word["translation"],
                "transliteration": word["transliteration"],
                "difficulty": 1  # All common words start at difficulty 1
            })
        
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
        
        # Get the specific lesson with phrases
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
            
        # For mnemonics lesson, fetch words from phrases table
        if lesson.lesson_type == "mnemonics":
            logger.debug("Found mnemonics lesson")
            phrases = db.query(models.Phrase).filter(
                models.Phrase.lesson_id == lesson.id
            ).all()
            
            # Convert phrases to practice_words format
            content["practice_words"] = [
                {
                    "word": phrase.text,
                    "translation": phrase.translation,
                    "transliteration": phrase.transliteration,
                    "mnemonic": phrase.extra_data.get("mnemonic", "") if phrase.extra_data else ""
                }
                for phrase in phrases
            ]
            logger.debug(f"Found {len(content['practice_words'])} practice words")
            logger.debug(f"Practice words: {content['practice_words']}")
        else:
            # Convert practice_words to words if needed
            if "practice_words" in content and not content.get("words"):
                content["words"] = content["practice_words"]
                
            # Ensure words is a list and preserve mnemonic/context fields
            if "words" not in content or not isinstance(content["words"], list):
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
                        processed_word = {
                            "word": word.get("word", ""),
                            "translation": word.get("translation", ""),
                            "transliteration": word.get("transliteration", ""),
                        }
                        if "mnemonic" in word:
                            processed_word["mnemonic"] = word["mnemonic"]
                        if "context" in word:
                            processed_word["context"] = word["context"]
                        processed_words.append(processed_word)
                    else:
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
            content=content,
            language_id=lesson.language_id,
            lesson_type=lesson.lesson_type,
            phrases=lesson.phrases  # Include phrases in response
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
        logger.error(f"Traceback: {traceback.format_exc()}")
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
                "lesson_type": "visual",
                "visualization_description": "In this lesson, you will learn Greek vocabulary by associating words with vivid and memorable visual images. Each word is paired with a descriptive hint to help you create a mental picture, enhancing your ability to remember and recall the word's meaning and pronunciation."
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
                    # Create visual lesson words with their hints
                    visual_words = []
                    for word in popularGreekWords[75:100]:
                        visual_word = word.copy()  # Create a copy of the word dictionary
                        if visual_word["word"] in visual_hints:
                            visual_word["visual_hint"] = visual_hints[visual_word["word"]]
                        visual_words.append(visual_word)
                    words = visual_words
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

@router.post("/lessons/initialize-greek")
def initialize_greek_lessons(response: Response, db: Session = Depends(get_db)):
    """Initialize Greek language lessons with rate limit handling"""
    try:
        with handle_rate_limit():
            # Check if lessons already exist
            existing_lessons = db.query(models.Lesson).filter(
                models.Lesson.language_code == "el"
            ).count()
            
            if existing_lessons > 0:
                return {"message": "Greek lessons already initialized"}
            
            # Initialize lessons with rate limit handling
            lessons = []
            
            # Add each lesson type with rate limit handling
            lesson_types = ["alphabet", "greetings", "visual", "mnemonics"]
            
            for lesson_type in lesson_types:
                with handle_rate_limit():
                    lesson_content = generate_lesson_content(lesson_type, [], "A1")
                    lesson = models.Lesson(
                        title=f"Greek {lesson_type.capitalize()} Lesson",
                        description=f"Learn Greek through {lesson_type}",
                        language_code="el",
                        lesson_type=lesson_type,
                        level="A1",
                        content=lesson_content
                    )
                    lessons.append(lesson)
            
            # Add all lessons to database
            db.add_all(lessons)
            db.commit()
            
            return {"message": "Greek lessons initialized successfully"}
            
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error initializing Greek lessons: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing lessons: {str(e)}"
        )

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
            
        # Clean up existing lessons
        existing_lessons = db.query(models.Lesson).filter(models.Lesson.language_id == greek.id).all()
        for lesson in existing_lessons:
            db.delete(lesson)
        db.commit()
        logger.debug("Cleaned up existing lessons")
        
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
                "description": "Learn essential Greek greetings and farewells, from formal situations to casual conversations",
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
                "lesson_type": "visual",
                "visualization_description": "In this lesson, you will learn Greek vocabulary by associating words with vivid and memorable visual images. Each word is paired with a descriptive hint to help you create a mental picture, enhancing your ability to remember and recall the word's meaning and pronunciation."
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
                    words = greek_greetings
                elif config["lesson_type"] == "spaced_repetition":
                    words = popularGreekWords[:25]
                elif config["lesson_type"] == "mnemonics":
                    words = popularGreekWords[25:50]
                    logger.debug(f"Mnemonic words selected: {words}")  # Log selected words
                elif config["lesson_type"] == "contextual":
                    words = popularGreekWords[50:75]
                elif config["lesson_type"] == "visual":
                    # Create visual lesson words with their hints
                    visual_words = []
                    for word in popularGreekWords[75:100]:
                        visual_word = word.copy()  # Create a copy of the word dictionary
                        if visual_word["word"] in visual_hints:
                            visual_word["visual_hint"] = visual_hints[visual_word["word"]]
                        visual_words.append(visual_word)
                    words = visual_words
                else:
                    words = []
                
                # Generate content for the lesson
                content = generate_lesson_content(config["lesson_type"], words, config["level"])
                logger.debug(f"Generated content for {config['title']}: {content}")
                
                # Create new lesson
                lesson = models.Lesson(
                    title=config["title"],
                    description=config["description"],
                    level=config["level"],
                    category=config["category"],
                    lesson_type=config["lesson_type"],
                    content=content,  # Use the generated content from generate_lesson_content
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
