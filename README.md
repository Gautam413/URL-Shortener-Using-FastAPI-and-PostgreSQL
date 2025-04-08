
# URL Shortener using FastAPI and PostgreSQL

This is a secure and feature-rich URL shortener built using FastAPI and PostgreSQL. The project supports:
- Email-based access control
- Expiration of short URLs
- Access logging
- Email notifications to creators

## Features

- Secure access via email-based verification
- URL expiration support
- Email notifications
- Access logging
- PostgreSQL + Alembic for migrations

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- Git (optional, for cloning)

### Clone the repository

```bash
git clone https://github.com/Gautam413/URL-Shortener-Using-FastAPI-and-PostgreSQL.git
cd URL-Shortener-Using-FastAPI-and-PostgreSQL
```

### Create and activate virtual environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate
```

```bash
# On Linux/macOS
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set up PostgreSQL

Create a PostgreSQL database and create the `.env` file with your credentials:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
EMAIL_USERNAME="your_email@example.com"
EMAIL_PASSWORD="your_password"
SMTP_SERVER="smtp.example.com"
SMTP_PORT=465
JWT_SECRET=12345678 #any according to your preference
```

### Run migrations using Alembic

```bash
alembic upgrade head
```

### Run the application

```bash
python -m uvicorn main:app --reload
```

The app will be available at `http://127.0.0.1:8000`

## Project Structure
```
.
├── alembic/
├── static/
├── templates/
├── main.py
├── crud.py
├── models.py
├── schemas.py
├── database.py
├── email_utils.py
├── requirements.txt
└── .env
```
