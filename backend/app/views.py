import json

import pika
from flask import jsonify, request
from mongoengine import DoesNotExist, OperationError
from pika.exceptions import ConnectionClosed

from app import app, pika_connection
from app.models import Task

from .config import config


def _success_envelope(payload):
    return jsonify({'status': 1, 'payload': payload})


def _error_envelope(error_title, error_message):
    return jsonify({'status': 0, 'error_title': error_title, 'error_message': error_message})


def _task_serializer(task: Task):
    return dict(id=str(task.id), name=task.name, status=task.status)


def _queue_publish(payload, queue=None):
    if not queue:
        return

    global pika_connection
    try:
        channel = pika_connection.channel()
    except:
        app.logger.info('reconnect')
        pika_connection = pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_URL))
        channel = pika_connection.channel()

    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(payload))


@app.route('/tasks', methods=['POST'])
def add_task():
    """Create a task. The initial status of the 'task' is 'initialized'.
    Also fire an event to the queue for further processing but the consumer.
        ---
        parameters:
          - name: name
            in: query
            type: string
            required: true
            default: untitled
        definitions:
          Task:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              status:
                type: string
          TaskSuccess:
            type: object
            properties:
              payload:
                $ref: '#/definitions/Task'
              status: 1

        responses:
          200:
            description: The created Task object
            schema:
              $ref: '#/definitions/TaskSuccess'

    """

    name = request.values.get('name')

    task = Task(name=name)

    task.save()

    # Notify
    _queue_publish({'task_id': str(task.id)}, queue='initialized')

    return _success_envelope(_task_serializer(task))


@app.route('/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task. Also used by the queue to update the status of the task.
        ---
        parameters:
          - name: task_id
            in: path
            type: string
            required: true

          - name: name
            in: query
            type: string
            required: true
            default: untitled

          - name: status
            in: query
            type: string
            required: true
            default: processing
          - name: consumer_queue
            in: query
            type: string
            required: true
            description: Only to be used by the queues

        responses:
          200:
            description: The created Task object
            schema:
              $ref: '#/definitions/TaskSuccess'

    """
    name = request.values.get('name')
    status = request.values.get('status')
    consumer_queue = request.values.get('consumer_queue')

    try:
        task = Task.objects.get(id=task_id)
    except DoesNotExist:
        return

    if name is not None:
        task.name = name

    if status is not None:
        task.status = status

    # After successful consumer message, route it to the next queue
    next_queue = None
    if consumer_queue == 'initialized':
        next_queue = 'processing'
        task.status = 'processing'

    task.save()

    # Notify
    _queue_publish({'task_id': str(task.id)}, queue=next_queue)

    return _success_envelope(_task_serializer(task))


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get a list of tasks.
        ---
        definitions:
          TaskSuccessArray:
            type: array
            items:
              $ref: '#/definitions/Task'

        responses:
          200:
            description: The created Task object
            schema:
              $ref: '#/definitions/TaskSuccessArray'

    """
    return _success_envelope([_task_serializer(task) for task in list(Task.objects)])


@app.route('/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task
        ---
        parameters:
          - name: task_id
            in: path
            type: string
            required: true

        responses:
          200:
            description: The fetched Task object
            schema:
              $ref: '#/definitions/TaskSuccess'

    """
    try:
        task = Task.objects.get(id=task_id)
    except DoesNotExist:
        return _error_envelope(error_title='DOES NOT EXIST', error_message='Task does not exist')

    return _success_envelope(_task_serializer(task))


@app.route('/task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a single task
        ---
        parameters:
          - name: task_id
            in: path
            type: string
            required: true
    """
    try:
        task = Task.objects.get(id=task_id)
    except DoesNotExist:
        return _error_envelope(error_title='DOES NOT EXIST', error_message='Task does not exist')
    try:
        task.delete()
    except OperationError:
        return _error_envelope(error_title='DELETE FAILED', error_message='Delete operation failed')

    return _success_envelope({})
