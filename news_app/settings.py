"""
Central configuration for the News Application project.

What this file is for:
- This file tells Django how the whole project should behave.
- It decides which apps are installed, where templates live, which database is
  used, and which custom user model the project trusts.

How this file connects to the rest of the project:
- `INSTALLED_APPS` must list `accounts`, `core`, and `api`.
- `AUTH_USER_MODEL` points all authentication logic to `accounts.CustomUser`.
- `TEMPLATES` tells Django where shared HTML files such as `base.html` live.
- `DATABASES` starts with SQLite now, but this is where you later switch to
  MariaDB for the capstone requirement.

Concepts used in this file:
- Project-level configuration
- Template discovery
- Static files
- Authentication
- Database configuration
- REST framework defaults
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# Development-only settings.
# TODO: Move sensitive values into environment variables before deployment.
SECRET_KEY = "django-insecure-f&l0bgx*er01n24gg=0(idutw3tcq*1u^=b8!#%($1*s$y7x=-"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "accounts",
    "core",
    "api",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "news_app.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Shared templates such as `base.html` and `registration/login.html`
        # live here.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "news_app.wsgi.application"
ASGI_APPLICATION = "news_app.asgi.application"


# Start with SQLite while scaffolding the project.
# TODO: Replace this block with a MariaDB connection before final submission.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_USER_MODEL = "accounts.CustomUser"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# TODO: Replace the console backend with a real email provider later.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "newsroom@example.com"


LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "core:home"
LOGIN_URL = "accounts:login"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
