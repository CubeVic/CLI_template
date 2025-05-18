FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \ 
    POETRY_VIRTUALENVS_CREATE=false

# install ddependencies 
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY . /app

ENTRYPOINT ["poetry", "run", "cli-template"]

