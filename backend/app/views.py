from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from . import app, db
from .decorators import require_api_key
from .models import Task

from .config import config
from .queue import queue_push
from .responses import success_envelope, error_envelope


def _task_serializer(task: Task):
    return dict(id=str(task.id), name=task.name, status=task.status)


@app.route('/tasks', methods=['POST'])
@require_api_key()
def add_task():
    """Create a task. The initial status of the 'task' is 'initialized'.
    Also fire an event to the queue for further processing but the consumer.
        ---

        parameters:
          - name: X-Api-Key
            in: header
            required: true
            description: Required API Key. Find the API Key in the Web Env file in the envs folder..

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

    task = Task(name=name, status='initialized')
    db.session.add(task)
    db.session.commit()

    # Notify
    queue_push({'task_id': str(task.id)}, queue='initialized')

    return success_envelope(_task_serializer(task))


@app.route('/task/<task_id>', methods=['PUT'])
@require_api_key()
def update_task(task_id):
    """Update a task. Also used by the queue to update the status of the task.
        ---
        parameters:
          - name: X-Api-Key
            in: header
            required: true
            description: Required API Key. Find the API Key in the Web Env file in the envs folder..

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
        task = Task.query.get(task_id)
    except NoResultFound:
        return error_envelope('DOES NOT EXIST', 'Task does not exist')

    if name is not None:
        task.name = name

    if status is not None:
        task.status = status

    # After successful consumer message, route it to the next queue
    next_queue = None
    if consumer_queue == 'initialized':
        next_queue = 'processing'
        task.status = 'processing'

    db.session.commit()

    # Notify
    queue_push({'task_id': str(task.id)}, queue=next_queue)

    return success_envelope(_task_serializer(task))


@app.route('/tasks', methods=['GET'])
@require_api_key()
def get_tasks():
    """Get a list of tasks.
        ---
        parameters:
          - name: X-Api-Key
            in: header
            required: true
            description: Required API Key. Find the API Key in the Web Env file in the envs folder..

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
    return success_envelope([_task_serializer(task) for task in list(Task.query.all())])


@app.route('/task/<task_id>', methods=['GET'])
@require_api_key()
def get_task(task_id):
    """Get a single task
        ---
        parameters:
          - name: task_id
            in: path
            type: string
            required: true
            description: Required API Key. Find the API Key in the Web Env file in the envs folder..

          - name: X-Api-Key
            in: header
            required: true

        responses:
          200:
            description: The fetched Task object
            schema:
              $ref: '#/definitions/TaskSuccess'

    """
    try:
        task = Task.query.get(task_id)
    except NoResultFound:
        return error_envelope(error_title='DOES NOT EXIST', error_message='Task does not exist')

    return success_envelope(_task_serializer(task))


@app.route('/task/<task_id>', methods=['DELETE'])
@require_api_key()
def delete_task(task_id):
    """Delete a single task
        ---
        parameters:
          - name: task_id
            in: path
            type: string
            required: true

          - name: X-Api-Key
            in: header
            required: true
            description: Required API Key. Find the API Key in the Web Env file in the envs folder..
    """
    try:
        task = Task.query.get(task_id)
    except NoResultFound:
        return error_envelope(error_title='DOES NOT EXIST', error_message='Task does not exist')
    try:
        db.session.delete(task)
    except IntegrityError:
        return error_envelope(error_title='DELETE FAILED', error_message='Delete operation failed')

    return success_envelope({})
