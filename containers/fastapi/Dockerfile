FROM ghcr.io/astral-sh/uv:python3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY application/pyproject.toml /code/
RUN uv sync
