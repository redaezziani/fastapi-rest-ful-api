from sqlalchemy import Column, Integer, String
from database import Base



import uuid
from sqlalchemy import Column, String, TIMESTAMP, Boolean, ForeignKey, Index ,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from database import Base

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    manga_Name = Column(String)
    chapter_number = Column(Integer, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'))

    __table_args__ = (
        Index('idx_chapter_manga_id_number', "chapter_number"),
    )


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

