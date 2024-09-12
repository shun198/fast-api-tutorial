FROM tiangolo/uvicorn-gunicorn:python3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY application/pyproject.toml /code/
RUN pip install --upgrade pip && pip install poetry
RUN poetry install
COPY application/ /code/
