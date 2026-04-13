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

## Local Setup

Start from a terminal in the folder where you want to keep the project:

```powershell
git clone <your-repository-url> news_app
cd news_app
```

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install the dependencies

```powershell
pip install -r requirements.txt
```

### 3. Create a `.env` file

Copy the example file and update it with your own values:

```powershell
Copy-Item .env.example .env
```

The project now loads `.env` automatically from the repository root by using
`python-dotenv`.

### 4. Choose a database setup

#### Option A: MariaDB (recommended for the capstone review)

Create the MariaDB database before running migrations:

```sql
CREATE DATABASE news_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then make sure your `.env` contains the correct MariaDB connection details:

```env
DJANGO_SECRET_KEY=replace-this-with-a-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
NEWS_APP_DB_ENGINE=mariadb
NEWS_APP_DB_NAME=news_app
NEWS_APP_DB_USER=root
NEWS_APP_DB_PASSWORD=change-me
NEWS_APP_DB_HOST=127.0.0.1
NEWS_APP_DB_PORT=3306
```

#### Option B: SQLite (quick local setup)

If you want to run the project without MariaDB, update `.env` to use SQLite:

```env
DJANGO_SECRET_KEY=replace-this-with-a-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
NEWS_APP_DB_ENGINE=sqlite
```

When `NEWS_APP_DB_ENGINE=sqlite`, Django will create `db.sqlite3` automatically
when you run migrations.

### 5. Apply migrations and seed the role groups

```powershell
python manage.py migrate
python manage.py seed_groups
python manage.py createsuperuser
python manage.py runserver
```

Open the app at `http://127.0.0.1:8000/`.

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

Open a terminal in the project root first, the same directory that contains
`Dockerfile` and `manage.py`:

```powershell
cd path\to\news_app
```

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
