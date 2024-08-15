FROM python:3.12-slim

WORKDIR app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./fake_api_other_services/requirements.txt requirements.txt

RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY ./fake_api_other_services/src .

ENTRYPOINT ["gunicorn", "main:app", "--bind", "0.0.0.0:8002", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
