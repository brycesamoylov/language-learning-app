from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/languages",
    tags=["languages"]
)

@router.get("/", response_model=List[schemas.Language])
def get_languages(db: Session = Depends(get_db)):
    """Get all available languages"""
    try:
        logger.debug("Fetching all languages")
        languages = db.query(models.Language).all()
        logger.debug(f"Found {len(languages)} languages")
        return languages
    except Exception as e:
        logger.error(f"Error fetching languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
