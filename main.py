from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import shortuuid
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import get_db, engine
from models import Base, ShortURL, AccessLog
from schemas import URLCreate, AccessRequest
from email_utils import send_verification_email, notify_creator
from datetime import datetime
import jwt 
from starlette.responses import RedirectResponse
import os


from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

SECRET_KEY = os.getenv("JWT_SECRET")

app = FastAPI()
app.state.limiter = limiter  

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"message": "Too many requests. Please try again later."})

@app.get("/")
@limiter.limit("10/minute")  # 10 requests per minute
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten")
@limiter.limit("5/minute")  # Limit to 5 shorten requests per minute
def create_short_url(request: Request, data: URLCreate, db: Session = Depends(get_db)):
    short_url = shortuuid.ShortUUID().random(length=6)

    new_url = ShortURL(
        short_url=short_url,
        original_url=data.original_url,
        creator_email=data.creator_email,
        authorized_emails=",".join(data.authorized_emails)
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    shortened_link = f"http://127.0.0.1:8000/{short_url}"
    return {"short_url": shortened_link}

@app.get("/{short_url}") 
def access_url(short_url: str, request: Request, db: Session = Depends(get_db)):
    short_url_entry = db.query(ShortURL).filter(ShortURL.short_url == short_url).first()

    if not short_url_entry:
        raise HTTPException(status_code=404, detail="Shortened URL not found in the database.")

    return templates.TemplateResponse("access_form.html", {"request": request, "short_url": short_url})

@app.post("/{short_url}/request-access")
@limiter.limit("3/minute")  # Limit to 3 email requests per minute
def request_access(short_url: str, data: AccessRequest, request: Request, db: Session = Depends(get_db)):
    """
    Handles the access request and sends a verification email.
    """
    short_url_entry = db.query(ShortURL).filter(ShortURL.short_url == short_url).first()
    if not short_url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found.")

    authorized_emails = short_url_entry.authorized_emails.split(",")
    if data.user_email not in authorized_emails:
        raise HTTPException(status_code=403, detail="You are not authorized to access this URL.")

    send_verification_email(data.user_email, short_url)
    return {"message": "Verification email sent. Please check your inbox."}

@app.get("/verify/{token}")
@limiter.limit("10/minute")  # Limit token verification attempts
def verify_access(token: str, request: Request, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        short_url = payload["short_url"]
        user_email = payload["user_email"]

        short_url_entry = db.query(ShortURL).filter(ShortURL.short_url == short_url).first()
        if not short_url_entry:
            raise HTTPException(status_code=404, detail="Short URL not found.")

        # Log the access event
        new_log = AccessLog(short_url=short_url, accessed_by=user_email)
        db.add(new_log)
        db.commit()

        # Notify creator
        creator_email = short_url_entry.creator_email
        notify_creator(creator_email, user_email, short_url_entry.original_url)

        return RedirectResponse(url=short_url_entry.original_url)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Verification link expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid verification link.")
