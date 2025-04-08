import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session

import os
import random
import string
from datetime import datetime, timezone, timedelta

import jwt 
SECRET_KEY = os.getenv("JWT_SECRET") 

#Generate a unique verification token
def generate_token(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def send_email(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    email_user = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")





def generate_verification_token(email: str, short_url: str):
    payload = {
        "user_email": email,
        "short_url": short_url,
        "exp": datetime.now(timezone.utc) + timedelta(days=1)  # 1-day expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# Send Verification Email with JWT
def send_verification_email(to_email: str, short_url: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    email_user = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")

    token = generate_verification_token(to_email, short_url)  #Generate JWT token
    verification_link = f"http://127.0.0.1:8000/verify/{token}"  #Use token in URL

    subject = "Verify Your Access"
    body = f"Click <a href='{verification_link}'>here</a> to verify your access. This link will expire in 24 hours."

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())
        server.quit()
        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def notify_creator(creator_email: str, user_email: str, original_url: str):
    subject = "Your Short URL Has Been Accessed"
    body = f"User {user_email} has accessed your short URL. <br>Original URL: {original_url}"

    send_email(creator_email, subject, body)
