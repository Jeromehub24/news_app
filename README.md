# News App

A Django news site with three roles:

- Readers can browse approved articles and follow publishers or journalists.
- Journalists can create articles and newsletters.
- Editors can review and approve articles before they are published.

## Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- SQLite for local development

## Run Locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_groups
python manage.py createsuperuser
python manage.py runserver
```

## API

- `/api/articles/feed/`
- `/api/publishers/`
