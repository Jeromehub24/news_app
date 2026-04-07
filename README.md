# News App Capstone

`news_app` is a Django capstone project for a role-based news publishing
workflow. Readers can browse approved content and follow publishers or
journalists, journalists can draft articles and newsletters, and editors can
review and approve articles before publication.

## Features

- Custom user roles: reader, journalist, and editor
- Publisher, article, and newsletter models
- Approval workflow for article publishing
- Web interface for browsing, writing, and reviewing content
- Subscription-based REST API feed for authenticated users

## Tech Stack

- Python 3.11
- Django 5.2
- Django REST Framework
- SQLite for local development
- MariaDB driver included for later database migration

## Project Structure

- `accounts/`: custom user model, signup/login flow, and role handling
- `core/`: publishers, articles, newsletters, and review workflow
- `api/`: authenticated API endpoints for publisher lists and article feeds
- `templates/` and `static/`: shared HTML, CSS, and JavaScript assets

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Seed the role groups:

   ```bash
   python manage.py seed_groups
   ```

5. Create an admin user if needed:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `GET /api/articles/feed/`: approved articles from followed publishers and journalists
- `GET /api/publishers/`: list of publishers

## Notes

- The repository excludes the local virtual environment and SQLite database so
  the project can be cloned cleanly.
- The current settings use SQLite in development and keep deployment-related
  values as TODO items for later hardening.
