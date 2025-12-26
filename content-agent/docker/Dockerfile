FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-root

COPY src /app/src
COPY data /app/data
COPY .env /app/.env

CMD ["poetry", "run", "python", "src/main.py"]
