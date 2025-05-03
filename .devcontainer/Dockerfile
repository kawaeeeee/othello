FROM python:3.12-bullseye AS backend-base  
# ベースイメージを Python 3.12 に変更

WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
# RUN curl -sSL https://install.python-poetry.org | python3 -

# ENV PATH="/root/.local/bin:$PATH"

FROM node:18-alpine AS frontend-base

WORKDIR /app

# RUN apk add --no-cache bash git curl

FROM backend-base AS backend-dev
COPY backend/pyproject.toml backend/poetry.lock backend/README.md ./

COPY backend/src ./src
# RUN poetry install --no-root
# 必要なライブラリをすべてインストール
ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/root/.local" \
    PYTHONUNBUFFERED=1
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install



FROM frontend-base AS frontend-dev
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm install

COPY frontend/ .

# 最終的な開発イメージ (両方の環境を含む)
FROM docker.io/library/debian:stable-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    # python3.12 \  
    # Python 3.10 を明示的にインストール
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/root/.local" \
    PYTHONUNBUFFERED=1
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - 
WORKDIR /workspace

COPY --from=backend-dev /app /workspace/backend
COPY --from=frontend-dev /app /workspace/frontend



# 必要に応じて追加のセットアップ
# RUN pip3 install --upgrade pip

# USER 1000:1000