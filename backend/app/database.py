from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
from .models import Lesson, Phrase
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

def add_memory_technique_lessons(db: Session, language_id: int):
    words_with_mnemonics = [
        {
            "word": "καλά",
            "translation": "good/well",
            "transliteration": "kala",
            "mnemonic": "Think of a CALm person saying 'Ah!' - they're feeling good (kala)"
        },
        {
            "word": "τώρα",
            "translation": "now",
            "transliteration": "tora",
            "mnemonic": "Think of a TORnado - it's happening right NOW (tora)"
        },
        {
            "word": "εδώ",
            "translation": "here",
            "transliteration": "edo",
            "mnemonic": "Imagine EDdie saying 'Oh!' - he's right HERE (edo)"
        },
        {
            "word": "μόνο",
            "translation": "only",
            "transliteration": "mono",
            "mnemonic": "Think of MONO sound - there's ONLY one channel (mono)"
        },
        {
            "word": "κάθε",
            "translation": "every",
            "transliteration": "kathe",
            "mnemonic": "Imagine a CAT saying 'Hey!' to EVERY other cat (kathe)"
        },
        {
            "word": "μέρα",
            "translation": "day",
            "transliteration": "mera",
            "mnemonic": "Think of a MERRY morning - it's a new DAY (mera)"
        },
        {
            "word": "ξέρω",
            "translation": "know",
            "transliteration": "ksero",
            "mnemonic": "Like a XEROX copy - you KNOW exactly what's on it (ksero)"
        },
        {
            "word": "πάλι",
            "translation": "again",
            "transliteration": "pali",
            "mnemonic": "Think of your PAL coming AGAIN (pali)"
        },
        {
            "word": "μετά",
            "translation": "after",
            "transliteration": "meta",
            "mnemonic": "Think META data comes AFTER the main data (meta)"
        },
        {
            "word": "πριν",
            "translation": "before",
            "transliteration": "prin",
            "mnemonic": "Think of a PRINCE who always comes BEFORE others (prin)"
        }
    ]

    lesson = Lesson(
        title="Mnemonic Devices for Greek",
        description="Learn to create memorable associations for Greek vocabulary using mnemonic devices",
        level="A1",
        category="Memory Techniques",
        lesson_type="mnemonics",
        content={
            "introduction": "Master Greek Words Through Memory Techniques",
            "description": "Each word comes with a mnemonic device to help you create strong mental connections and remember both meaning and pronunciation.",
            "activities": [
                "Create memorable associations",
                "Practice visualization techniques",
                "Connect words with similar sounds",
                "Build memory palaces"
            ],
            "words": words_with_mnemonics
        },
        language_id=language_id
    )
    
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

def init_db(db: Session, language_id: int):
    add_memory_technique_lessons(db, language_id)
