from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# User-Language association table
user_languages = Table(
    'user_languages', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    learning_languages = relationship("Language", secondary=user_languages)
    progress = relationship("Progress", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    native_language = Column(String)
    learning_goals = Column(JSON)
    daily_goal_minutes = Column(Integer, default=30)
    level = Column(Integer, default=1)
    points = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    user = relationship("User", back_populates="profile")

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(2), unique=True, index=True)  # ISO 639-1 code
    name = Column(String(50), nullable=False)
    native_name = Column(String(50), nullable=True)
    flag = Column(String(10), nullable=True)
    rtl = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lessons = relationship("Lesson", back_populates="language", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    description = Column(String(500), index=True)
    level = Column(String(2), index=True)  # A1, A2, B1, B2, C1, C2
    category = Column(String(50), index=True)
    lesson_type = Column(String(50), index=True)
    content = Column(JSON)
    language_id = Column(Integer, ForeignKey("languages.id"))
    language = relationship("Language", back_populates="lessons")
    phrases = relationship("Phrase", back_populates="lesson", cascade="all, delete-orphan")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, title, description, level=None, category=None, lesson_type=None, content=None, language_id=None):
        self.title = title
        self.description = description
        self.level = level
        self.category = category
        self.lesson_type = lesson_type
        self.content = content
        self.language_id = language_id

    @staticmethod
    def create_popular_words_lesson(language_id):
        return Lesson(
            title="100 Most Popular Greek Words",
            description="Learn the most commonly used Greek words.",
            level="Beginner",
            category="Popular Words",
            content={},
            language_id=language_id
        )

class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    transliteration = Column(Text)
    translation = Column(Text)
    level = Column(String(2))
    category = Column(String(50))
    language_id = Column(Integer, ForeignKey("languages.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    lesson = relationship("Lesson", back_populates="phrases")
    audio_url = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    completed = Column(Boolean, default=False)
    score = Column(Integer)
    completed_at = Column(DateTime)
    user = relationship("User", back_populates="progress")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    earned_at = Column(DateTime, default=datetime.utcnow)
    badge_image_url = Column(String)
    user = relationship("User", back_populates="achievements")

class VocabularyItem(Base):
    __tablename__ = "vocabulary_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    language_id = Column(Integer, ForeignKey("languages.id"))
    word = Column(String)
    translation = Column(String)
    context = Column(String)
    category = Column(String)
    mastery_level = Column(Integer, default=0)
    last_reviewed = Column(DateTime)
