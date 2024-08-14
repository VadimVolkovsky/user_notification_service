FROM python:3.12-slim

WORKDIR app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

COPY src/requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY . .

