FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock  src/ ./
COPY . .

RUN poetry install --only main --no-root

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]
