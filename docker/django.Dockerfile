FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        gcc \
        netcat-openbsd \ 
        pkg-config \ 
        libmariadb-dev-compat \
        libmariadb-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

COPY Pipfile Pipfile.lock* ./

RUN pipenv install --deploy --ignore-pipfile

COPY . .

RUN chmod +x /app/entrypoint.sh

RUN pipenv run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["pipenv", "run", "gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]