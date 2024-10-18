# router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter(
    prefix="/chapters",
    tags=["Chapters"]
)


@router.get("/")
def get_all_chapters(db: Session = Depends(get_db)):
    chapters = db.query(models.Chapter).all()
    return chapters

@router.get("/{chapter_id}")
def get_chapter_by_id(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()

    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return chapter
