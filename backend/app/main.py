from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from . import models
from .database import engine, SessionLocal
from .routers import lessons, languages
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

# Drop and recreate all tables
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

# Initialize Greek language
from sqlalchemy.orm import Session
db = SessionLocal()
try:
    # Create Greek language if it doesn't exist
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
    logger.info("Created Greek language entry")
except Exception as e:
    logger.error(f"Error creating Greek language: {str(e)}")
    db.rollback()
finally:
    db.close()

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://127.0.0.1:3000",
    "127.0.0.1:3000",
    "*"  # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler for logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Include routers
app.include_router(lessons.router)
app.include_router(languages.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Language Learning API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
