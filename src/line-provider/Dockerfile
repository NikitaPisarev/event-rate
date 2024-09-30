FROM python:3.11-slim

RUN pip install poetry==1.8.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["sh", "entrypoint.sh"]
