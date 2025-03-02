FROM python:3.13 AS base

LABEL org.opencontainers.image.authors="Igor I Shatunov"
LABEL org.opencontainers.image.source=https://github.com/raider444/psytican-bot
LABEL org.opencontainers.image.description="Psytican chat helper bot image"
LABEL org.opencontainers.image.licenses=MIT

ARG POETRY_VERSION=2.0.1 \
    POETRY_HOME=/usr/local

RUN mkdir -p /opt/psytican/psytican-bot \
    && addgroup --gid 2000 psytican \
    && useradd -d /opt/psytican -s /bin/bash -g psytican -u 2000 psytican \
    && chown -R psytican:psytican /opt/psytican \
    && apt-get update -y \
    && apt-get install -y \
        curl \
    && pip install setuptools \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR /opt/psytican/psytican-bot

COPY pyproject.toml poetry.lock* setup.cfg ./

RUN poetry install --no-ansi --no-root --without=dev


FROM python:3.13-alpine AS production

ARG BOT_VERSION

LABEL org.opencontainers.image.authors="Igor I Shatunov"
LABEL org.opencontainers.image.source=https://github.com/raider444/psytican-bot
LABEL org.opencontainers.image.description="Psytican chat helper bot image"
LABEL org.opencontainers.image.licenses=MIT

ENV PORT=8000
RUN mkdir -p /opt/psytican/psytican-bot \
    && addgroup -g 2000 psytican \
    && adduser -h /opt/psytican -s /bin/ash -G psytican -u 2000 -D psytican \
    && chown -R psytican:psytican /opt/psytican \
    && pip install psytican-bot==${BOT_VERSION}

WORKDIR /opt/psytican/psytican-bot
USER psytican

ENTRYPOINT [ "psytican-bot" ]


FROM base AS develop

ARG DEV_VERSION=2024.0-dev

ENV PYTHONPATH="/opt/psytican/psytican-bot"
ENV PORT=8000

COPY . .
RUN poetry build \
    && poetry version ${DEV_VERSION}\
    && poetry install --no-ansi

ENTRYPOINT [ "psytican-bot" ]
