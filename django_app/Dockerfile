FROM python:3.14-slim
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY django_app .
RUN poetry run python manage.py collectstatic --no-input
CMD ["poetry", "run", "daphne", "-b", "0.0.0.0", "-p", "8000", "django_app.asgi:application"]