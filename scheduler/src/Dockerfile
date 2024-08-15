FROM python:3.12

RUN mkdir /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt app/requirements.txt
COPY deploy.sh app/deploy.sh

RUN  pip install --upgrade pip \
     && pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app
COPY ../.. /app

CMD ["bash", "deploy.sh"]
