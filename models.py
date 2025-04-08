from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone, timedelta

class ShortURL(Base):
    __tablename__ = "short_urls"
    
    short_url = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    creator_email = Column(String, nullable=False)
    authorized_emails = Column(String, nullable=False)  # Comma-separated
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(days=60))

class AccessLog(Base):
    
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Changed to Integer
    short_url = Column(String, nullable=False)
    accessed_by = Column(String, nullable=False)
    accessed_at = Column(DateTime, default=datetime.now(timezone.utc))  # Using utcnow directly

