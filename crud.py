from sqlalchemy.orm import Session
from models import ShortURL, VerificationToken
from schemas import URLCreate
import random
import string
from datetime import datetime, timezone

# Generate short URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Delete expired URLs
def delete_expired_urls(db: Session):
    db.query(ShortURL).filter(ShortURL.expires_at < datetime.now(timezone.utc)).delete()
    db.commit()

# Delete expired verification tokens
def delete_expired_tokens(db: Session):
    db.query(VerificationToken).filter(VerificationToken.expires_at < datetime.now(timezone.utc)).delete()
    db.commit()

# Create new short URL
def create_short_url(db: Session, url_data: URLCreate):
    delete_expired_urls(db)  # ✅ Remove old expired URLs
    short_url = generate_short_url()
    db_url = ShortURL(original_url=url_data.original_url, short_url=short_url, creator_email=url_data.creator_email, authorized_emails=",".join(url_data.authorized_emails))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
