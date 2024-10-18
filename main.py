from fastapi import FastAPI
from router import router as chapter_router  
from auth_router import router as auth_router 
from lib import MangaScraper

app = FastAPI()

from database import Base, engine

Base.metadata.create_all(bind=engine)
app.include_router(chapter_router)  
app.include_router(auth_router)

@app.get("/download_chapter")
def download_chapter(name: str, chapter: int):
    scraper = MangaScraper()
    return scraper.download_chapter(name, chapter)

@app.get("/download_manga_from_to")
def download_manga_from_to(name: str, start: int, end: int):
    scraper = MangaScraper()
    return scraper.download_manga_from_to(name, start, end)
