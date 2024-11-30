from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfileBase(BaseModel):
    native_language: str
    learning_goals: Dict
    daily_goal_minutes: int = 30

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int
    level: int
    points: int
    streak_days: int

    class Config:
        from_attributes = True

class PhraseBase(BaseModel):
    text: str
    transliteration: str
    translation: str
    level: str
    category: str
    extra_data: Optional[Dict] = None

class PhraseCreate(PhraseBase):
    language_id: int
    lesson_id: Optional[int] = None

class Phrase(PhraseBase):
    id: int
    language_id: int
    lesson_id: Optional[int] = None
    audio_url: Optional[str] = None
    extra_data: Optional[Dict] = None

    class Config:
        from_attributes = True

class LessonBase(BaseModel):
    title: str
    description: str
    level: Optional[str]
    category: Optional[str]
    lesson_type: Optional[str]
    content: Optional[Dict]

class LessonCreate(LessonBase):
    language_id: int

class Lesson(LessonBase):
    id: int
    language_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LessonDetail(LessonBase):
    id: int
    language_id: int
    content: Dict[str, Any]  # This will include practice_words and other content
    phrases: List[Phrase] = []  # Update to use Phrase schema
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProgressBase(BaseModel):
    lesson_id: int
    completed: bool
    score: Optional[int] = None

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class VocabularyItemBase(BaseModel):
    word: str
    translation: str
    context: Optional[str]
    category: str

class VocabularyItemCreate(VocabularyItemBase):
    language_id: int

class VocabularyItem(VocabularyItemBase):
    id: int
    user_id: int
    mastery_level: int
    last_reviewed: Optional[datetime]

    class Config:
        from_attributes = True

class Language(BaseModel):
    id: int
    code: str
    name: str
    native_name: Optional[str]
    flag: Optional[str]
    rtl: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
