FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV LISTEN_PORT 5000

EXPOSE 5000

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ../requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && newrelic-admin generate-config $NEWRELIC_KEY /app/newrelic.ini

COPY ./backend/supervisord.ini /etc/supervisor.d/supervisord.ini

COPY ./backend /app

#todo Add docker in-built healthcheck