from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from .models import Lesson
from .data.vocabulary import popularGreekWords

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./language_learning.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_popular_words_lesson(db: Session, language_id: int):
    popular_words_lesson = Lesson(
        title="100 Most Popular Greek Words",
        description="Learn the most commonly used Greek words.",
        level="Beginner",
        category="Popular Words",
        lesson_type="popular_words",
        content={
            "introduction": "These are the most frequently used words in Greek. Learning these will give you a strong foundation.",
            "description": "Start with these common words to quickly build your Greek vocabulary.",
            "practice_words": popularGreekWords  # Add all popular words
        },
        language_id=language_id
    )
    db.add(popular_words_lesson)
    db.commit()
    db.refresh(popular_words_lesson)
    return popular_words_lesson

def add_memory_technique_lessons(db: Session, language_id: int):
    # Spaced Repetition Lesson
    spaced_repetition_lesson = Lesson(
        title="Spaced Repetition Practice",
        description="Master Greek vocabulary through scientifically-proven spaced repetition technique.",
        level="A1",
        category="Memory Techniques",
        lesson_type="spaced_repetition",
        content={
            "introduction": "Spaced Repetition is a powerful memory technique that helps you learn and retain vocabulary effectively.",
            "description": "This technique involves reviewing words at increasing intervals over time. It leverages the psychological spacing effect, where information is more easily recalled if studied a few times over a long span rather than repeatedly in a short period.",
            "activities": [
                "Practice using spaced repetition apps like Anki or Quizlet.",
                "Review vocabulary words at increasing intervals.",
                "Test your recall of words in different contexts."
            ],
            "benefits": "Helps in long-term retention and reduces the forgetting curve by reinforcing memory just before it's about to fade.",
            "practice_words": popularGreekWords[:25]  # First 25 words for practice
        },
        language_id=language_id
    )

    # Mnemonics Lesson
    mnemonics_lesson = Lesson(
        title="Mnemonic Devices for Greek",
        description="Learn to create memorable associations for Greek vocabulary using mnemonic devices.",
        level="A1",
        category="Memory Techniques",
        lesson_type="mnemonics",
        content={
            "introduction": "Mnemonic devices are memory aids that help you remember words through associations.",
            "description": "Mnemonics are memory aids that help link new information to existing knowledge through vivid imagery, stories, or patterns. Each word below includes a mnemonic device to help you remember its meaning and pronunciation.",
            "example": "For the Greek word \"νερό\" (water), you might imagine a \"narrow\" stream of water to remember the pronunciation.",
            "benefits": "Makes learning more engaging and can significantly improve recall by creating strong mental connections.",
            "practice_words": [
                {
                    "word": word["word"],
                    "translation": word["translation"],
                    "transliteration": word["transliteration"],
                    "mnemonic": mnemonic
                }
                for word, mnemonic in zip(popularGreekWords[25:50], [
                    "Think 'kala-mari' (kala) - 'The calamari is good'",
                    "Think 'Torah' (tora) - 'Reading Torah right now'",
                    "Think 'edo(m)' (edo) - 'Here in the kingdom of Edom'",
                    "Think 'mono-rail' (mono) - 'Only one rail'",
                    "Think 'catheter' (kathe) - 'Every hospital has them'",
                    "Think 'mera-ngue' (mera) - 'A day for meringue'",
                    "Think 'Xerox' (ksero) - 'I know how to use a Xerox'",
                    "Think 'pally' (pali) - 'My pal is here again'",
                    "Think 'meta-data' (meta) - 'Comes after the data'",
                    "Think 'pre-in' (prin) - 'Before going in'",
                    "Think 'pan-o-rama' (pano) - 'View from above'",
                    "Think 'cat-o-nine' (kato) - 'Cat looking down'",
                    "Think 'maze-y' (mazi) - 'Together in the maze'",
                    "Think 'chorus' (horis) - 'Song without accompaniment'",
                    "Think 'nay' (ne) - 'Yes, I say nay to that'",
                    "Think 'oh hi' (ohi) - 'Oh hi, no thanks'",
                    "Think 'you-care-is-to' (efharisto) - 'Thank you for caring'",
                    "Think 'para-graph' (para) - 'Paragraphs are by the side'",
                    "Think 'poli-tics' (poli) - 'Many ticks in politics'",
                    "Think 'kane' (kane) - 'Do the cane dance'",
                    "Think 'pou-der' (pou) - 'Where is the powder?'",
                    "Think 'pou-te' (pote) - 'When is the party?'",
                    "Think 'kanis' (kanis) - 'No one can do it like Kanis'",
                    "Think 'kanenas' (kanenas) - 'No one is like Kanenas'",
                    "Think 'tipota' (tipota) - 'Nothing is like a teapot'"
                ])
            ]
        },
        language_id=language_id
    )

    # Contextual Learning Lesson
    contextual_lesson = Lesson(
        title="Contextual Learning",
        description="Learn Greek words naturally through context and real-world usage.",
        level="A1",
        category="Memory Techniques",
        content={
            "introduction": "Contextual learning helps you understand how words are used in real situations.",
            "description": "Learning words in context rather than in isolation helps to understand how they are used naturally. This approach mimics how we learn our native language.",
            "activities": [
                "Use words in sentences to practice context.",
                "Role-play scenarios using new vocabulary.",
                "Create stories incorporating new words."
            ],
            "benefits": "Enhances understanding of word usage, nuances, and collocations, making it easier to remember and apply vocabulary correctly.",
            "practice_words": [
                {
                    "word": word["word"],
                    "translation": word["translation"],
                    "transliteration": word["transliteration"],
                    "context": context
                }
                for word, context in zip(popularGreekWords[50:75], [
                    "At restaurants: First thing to order - 'Ena nero parakalo' (One water please)",
                    "At bakery: Point and say 'Afto to psomi parakalo' (This bread please)",
                    "Being hungry: Ask 'Ti fayito ehete?' (What food do you have?)",
                    "Coffee time: Ask for 'Me gala parakalo' (With milk please)",
                    "Dinner time: Order 'Ena krasi parakalo' (One wine please)",
                    "Morning ritual: Order 'Ena kafes sketo' (One plain coffee)",
                    "Dining: Say 'Ela sto trapezi' (Come to the table)",
                    "Hosting: Offer 'Kathise s'afti tin karekla' (Sit in this chair)",
                    "Bedtime: Say 'Pao sto krevati' (I'm going to bed)",
                    "Welcoming: Point to 'I porta ine eki' (The door is there)",
                    "Directions: Say 'To parathiro vlepi sti thalassa' (The window faces the sea)",
                    "House tour: Show 'Afto ine to domatio' (This is the room)",
                    "Cooking: Say 'I kouzina ine edo' (The kitchen is here)",
                    "Morning routine: Say 'Pao sto banio' (I'm going to the bathroom)",
                    "Directions: Ask 'Pou ine o dromos?' (Where is the street?)",
                    "Transport: Pao sto leoforio (I'm going to the bus)",
                    "Travel: Say 'Pao stin paralía' (I'm going to the beach)",
                    "Shopping: Ask 'Poso kanei afto?' (How much does this cost?)",
                    "Meeting: Say 'Chairo poli' (Nice to meet you)",
                    "Parting: Say 'Antio sas' (Goodbye)"
                ])
            ]
        },
        language_id=language_id
    )

    # Visual Association Lesson
    visual_lesson = Lesson(
        title="Visual Association Learning",
        description="Learn Greek words by creating strong visual mental images.",
        level="A1",
        category="Memory Techniques",
        content={
            "introduction": "Visual association is a powerful technique that helps you remember words by creating vivid mental images.",
            "description": "Our brains are wired to remember visual information better than text. By creating strong visual associations for each word, you can significantly improve your recall ability.",
            "activities": [
                "Visualize each word vividly.",
                "Draw or find images that represent words.",
                "Create a mental story using words."
            ],
            "benefits": "Visual associations create stronger neural connections, making it easier to recall words when needed.",
            "practice_words": [
                {
                    "word": word["word"],
                    "translation": word["translation"],
                    "transliteration": word["transliteration"],
                    "visual": visual
                }
                for word, visual in zip(popularGreekWords[75:100], [
                    "Picture a bright, golden sun (ήλιος) warming your face with its rays",
                    "Imagine a glowing crescent moon (φεγγάρι) casting silver light on a calm sea",
                    "Visualize a twinkling star (αστέρι) pulsing with different colors in the night sky",
                    "See a vast, blue sky (ουρανός) stretching endlessly above you",
                    "Picture a fluffy white cloud (σύννεφο) shaped like a playful rabbit",
                    "Imagine gentle rain (βροχή) creating ripples in a quiet pond",
                    "See soft, white snowflakes (χιόνι) dancing as they fall from the sky",
                    "Feel a refreshing breeze (άνεμος) rustling through your hair",
                    "Picture a bright red flower (λουλούδι) swaying in the wind",
                    "Imagine a lush green forest (δάσος) teeming with life",
                    "Visualize a calm, serene lake (λίμνη) reflecting the sky",
                    "See a majestic mountain (βουνό) rising into the clouds",
                    "Picture a vibrant rainbow (ουράνιο τόξο) arching across the sky",
                    "Imagine a bustling city (πόλη) alive with lights and sounds",
                    "Visualize a peaceful village (χωριό) nestled in a valley",
                    "See a vast ocean (ωκεανός) stretching to the horizon",
                    "Picture a golden beach (παραλία) with soft, warm sand",
                    "Imagine a dense jungle (ζούγκλα) filled with exotic plants",
                    "Visualize a tranquil garden (κήπος) blooming with flowers",
                    "See a grand palace (παλάτι) standing proudly"
                ])
            ],
            "example_situations": [
                "Nature Walk: Look at the 'ήλιος' (sun) in the 'ουρανός' (sky), spot 'πουλί' (birds) in the 'δέντρο' (trees)",
                "Garden Visit: Smell the 'λουλούδι' (flowers), watch the 'πεταλούδα' (butterfly) and 'μέλισσα' (bee)",
                "Fruit Picking: Collect 'μήλο' (apples), 'πορτοκάλι' (oranges), and 'φράουλα' (strawberries)",
                "Evening Sky: Watch the 'φεγγάρι' (moon) and 'αστέρι' (stars) appear"
            ]
        },
        language_id=language_id
    )

    # Add all lessons to database
    db.add(spaced_repetition_lesson)
    db.add(mnemonics_lesson)
    db.add(contextual_lesson)
    db.add(visual_lesson)
    db.commit()

    # Refresh all lessons
    db.refresh(spaced_repetition_lesson)
    db.refresh(mnemonics_lesson)
    db.refresh(contextual_lesson)
    db.refresh(visual_lesson)

    return [spaced_repetition_lesson, mnemonics_lesson, contextual_lesson, visual_lesson]


def add_greetings_lesson(db: Session, language_id: int):
    greetings_lesson = Lesson(
        title="Basic Greetings and Farewells",
        description="Learn essential Greek greetings and ways to say goodbye",
        language_id=language_id,
        level="A1",
        category="Basics",
        lesson_type="greetings",
        content={
            "words": [
                {
                    "word": "γεια σας",
                    "translation": "hello (formal)",
                    "transliteration": "ya sas",
                    "context": "Use this when greeting someone formally or multiple people"
                },
                {
                    "word": "γεια σου",
                    "translation": "hello (informal)",
                    "transliteration": "ya sou",
                    "context": "Use this when greeting one person informally"
                },
                {
                    "word": "αντίο",
                    "translation": "goodbye",
                    "transliteration": "adio",
                    "context": "Use this when parting ways"
                },
                {
                    "word": "καλημέρα",
                    "translation": "good morning",
                    "transliteration": "kalimera",
                    "context": "Use this greeting in the morning"
                },
                {
                    "word": "καλησπέρα",
                    "translation": "good afternoon/evening",
                    "transliteration": "kalispera",
                    "context": "Use this greeting in the afternoon or evening"
                },
                {
                    "word": "καληνύχτα",
                    "translation": "good night",
                    "transliteration": "kalinichta",
                    "context": "Use this when saying goodnight"
                }
            ]
        }
    )

    db.add(greetings_lesson)
    db.commit()
    db.refresh(greetings_lesson)

    return greetings_lesson


def init_db(db: Session, language_id: int):
    add_greetings_lesson(db, language_id)
    add_popular_words_lesson(db, language_id)
    add_memory_technique_lessons(db, language_id)
