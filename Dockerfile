FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=1
ENV DJANGO_ALLOWED_HOSTS=*
ENV NEWS_APP_DB_ENGINE=sqlite

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libmariadb-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_groups && python manage.py runserver 0.0.0.0:8000"]
