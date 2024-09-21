FROM python:3.12 as base

ARG POETRY_VERSION=1.4.2 \
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


FROM base as main

ENV PORT=8000

COPY . .
RUN poetry build \
    && poetry install --no-dev --no-ansi

ENTRYPOINT [ "psytican-bot" ]