FROM python:3.12

RUN mkdir /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'
#ENV PYTHONPATH .

#COPY .env /app/.env
COPY requirements.txt app/requirements.txt
COPY deploy.sh app/deploy.sh

RUN  pip install --upgrade pip \
     && pip install -r /app/requirements.txt --no-cache-dir


WORKDIR /app
COPY ../.. /app
#COPY src /app/src

CMD ["bash", "deploy.sh"]

# Run Celery
CMD ["celery", "-A", "celery", "worker", "--loglevel=info"]