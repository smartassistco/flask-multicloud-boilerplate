FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV LISTEN_PORT 5000

EXPOSE 5000

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./backend /app
