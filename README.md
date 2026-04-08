# News App

A Django news platform with separate reader, journalist, and editor workflows.

## Features

- Readers can follow publishers and journalists, then browse approved articles.
- Journalists can join publishers, submit articles, and draft newsletters.
- Editors can create publishers, approve articles, and update or delete articles
  and newsletters.
- A small REST API exposes publisher data and a personalized subscribed feed.

## Project Structure

- `accounts/` handles users, roles, and authentication workflows.
- `core/` contains publishers, articles, newsletters, and the main HTML views.
- `api/` exposes the reader-facing API endpoints.
- `docs/` contains the generated Sphinx documentation for the project.

## Local Setup With a Virtual Environment

1. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the project dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Provide your environment variables.

   Use `.env.example` as a guide. For a quick local setup you can run with
   SQLite instead of MariaDB by setting:

   ```powershell
   $env:DJANGO_SECRET_KEY = "replace-this-with-your-own-secret-key"
   $env:DJANGO_DEBUG = "1"
   $env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
   $env:NEWS_APP_DB_ENGINE = "sqlite"
   ```

   For a MariaDB-backed setup, also define:

   ```powershell
   $env:NEWS_APP_DB_NAME = "news_app"
   $env:NEWS_APP_DB_USER = "your-db-user"
   $env:NEWS_APP_DB_PASSWORD = "your-db-password"
   $env:NEWS_APP_DB_HOST = "127.0.0.1"
   $env:NEWS_APP_DB_PORT = "3306"
   ```

4. Apply migrations, seed the role groups, and start the app.

   ```bash
   python manage.py migrate
   python manage.py seed_groups
   python manage.py createsuperuser
   python manage.py runserver
   ```

5. Open the app at `http://127.0.0.1:8000/`.

## Documentation

The generated Sphinx HTML documentation is already included in the repository.
Open `docs/_build/html/index.html` in a browser to browse it.

To rebuild the docs:

```powershell
.\env_site\Scripts\python.exe -m pip install -U sphinx sphinx-rtd-theme
.\env_site\Scripts\sphinx-apidoc.exe -f -o docs . docs\* env_site\* accounts\migrations\* core\migrations\*
.\env_site\Scripts\sphinx-build.exe -M clean docs docs\_build
.\env_site\Scripts\sphinx-build.exe -M html docs docs\_build
```

## Running With Docker

Build the image:

```bash
docker build -t news-app-capstone .
```

Run the container:

```bash
docker run --rm -p 8000:8000 news-app-capstone
```

The Docker image defaults to SQLite for portability and runs migrations plus
`seed_groups` automatically before starting Django's development server.

## API Endpoints

- `/api/articles/feed/`
- `/api/publishers/`

## Security Note

No real passwords, tokens, or third-party credentials are committed to this
repository. Use your own values for database access, secret keys, and any future
external integrations.
