FROM python:3.12-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

RUN apt-get update \
    && apt-get install -y gcc libev4 libev-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend/core


FROM base AS dev_req

COPY pyproject.toml poetry.lock /app/backend/core/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/core/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


FROM base AS prod_req

COPY pyproject.toml poetry.lock /app/backend/core/

RUN python3 -m pip install poetry
COPY pyproject.toml poetry.lock /app/backend/core/

RUN poetry export --without-hashes --format=requirements.txt > requirements.txt


FROM base AS dev

COPY --from=dev_req /app/backend/core/requirements.txt /app/backend/core/

RUN pip install -r requirements.txt

COPY ./ /app/backend/core/
RUN chmod +x /app/backend/core/entrypoint.sh


FROM base AS prod

COPY --from=prod_req /app/backend/core/requirements.txt /app/backend/core/

RUN pip install -r requirements.txt

COPY ./ /app/backend/core/
RUN chmod +x /app/backend/core/entrypoint.sh
