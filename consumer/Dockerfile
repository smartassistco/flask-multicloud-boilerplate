FROM smartassist/py-consumer:redis

COPY ./consumer/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./consumer /app

ENV CONSUMER_IMPORT_PATH app.CONSUMERS
