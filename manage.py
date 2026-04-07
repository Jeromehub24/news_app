#!/usr/bin/env python
"""
Project entry point for the News Application Django project.

What this file is for:
- This is the file you run when you type commands such as
  `python manage.py runserver` or `python manage.py makemigrations`.
- It acts like the remote control for the Django project.

How this file connects to the rest of the project:
- It points Django to `news_app.settings`.
- After that, Django can discover the `accounts`, `core`, and `api` apps.

Concepts used in this file:
- Environment variables
- Command-line entry points
- Django management commands
"""

import os
import sys


def main():
    """
    Run administrative tasks.

    Step-by-step:
    1. Tell Django which settings file to use.
    2. Import Django's command runner.
    3. Pass through the command-line arguments you typed.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Install the packages in requirements.txt "
            "or activate the correct virtual environment before running "
            "manage.py commands."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
