# News App

A Django news site with separate reader, journalist, and editor workflows.

## Main Workflows

- Readers can follow publishers and journalists, then browse approved content.
- Journalists can join publishers, create articles, and draft newsletters.
- Editors can create publishers, join publisher teams, approve articles, and
  update or delete any article or newsletter.

## Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- MariaDB for normal development and review

## MariaDB Setup

Copy the values from `.env.example` into your shell before running the app.

PowerShell example:

```powershell
$env:DJANGO_SECRET_KEY = "replace-this-with-a-secret-key"
$env:DJANGO_DEBUG = "1"
$env:NEWS_APP_DB_ENGINE = "mariadb"
$env:NEWS_APP_DB_NAME = "news_app"
$env:NEWS_APP_DB_USER = "root"
$env:NEWS_APP_DB_PASSWORD = "change-me"
$env:NEWS_APP_DB_HOST = "127.0.0.1"
$env:NEWS_APP_DB_PORT = "3306"
```

Then run:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_groups
python manage.py createsuperuser
python manage.py runserver
```

The automated test suite falls back to SQLite so tests can run without a local
MariaDB service.

## API

- `/api/articles/feed/`
- `/api/publishers/`
