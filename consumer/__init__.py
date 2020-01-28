import json
import os
import random
import time

import requests

API_SERVER_HOST = os.getenv('API_SERVER_HOST')
API_KEY = os.getenv('API_KEY')


def _handle(message, current_queue, status=None):
    time.sleep(random.randint(0, 2))  # Random Delay for Demo
    task_id = json.loads(message)['task_id']
    data = {'consumer_queue': current_queue}
    if status:
        data.update(status=status)
    requests.put(API_SERVER_HOST + '/task/{}'.format(task_id),
                 data=data, headers={'X-Api-Key': API_KEY})  # todo Send Queue Ack only after a successful PUT


def handle_initialized(message):
    _handle(message, current_queue='initialized')


def handle_processing(message):
    if random.randint(0, 9) == 9:  # 90% Success 10% Failure
        result = 'failure'
    else:
        result = 'success'
    _handle(message, current_queue='processing', status=result)


CONSUMERS = [
    {
        'queue': 'initialized',
        'handler': handle_initialized,
    },
    {
        'queue': 'processing',
        'handler': handle_processing,
    },

]
