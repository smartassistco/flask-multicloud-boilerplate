import time

import pytest
import requests
import compose

from compose.container import Container

pytest_plugins = ["docker_compose"]


def _add_task(api_url, name='test_name'):
    api_url = api_url + 'tasks'
    print('API URL', api_url)
    response = requests.post(api_url, data={'name': name}).json()
    assert response['status'] == 1
    return response['payload']['id']


def _get_task(api_url, task_id):
    response = requests.get(api_url + 'task/{}'.format(task_id)).json()
    return response['payload']


def test_apis(function_scoped_container_getter):
    """

    """
    service = function_scoped_container_getter.get("web").network_info[0]
    api_url = "http://{}:{}/".format(service.hostname, service.host_port)

    name = 'test_name'

    time.sleep(12)  # Wait till containers are ready
    task_id = int(_add_task(api_url, name=name))

    while True:
        time.sleep(1)
        task = _get_task(api_url, task_id)
        assert task['name'] == name

        if task['status'] in ['success', 'failure']:
            break

        assert task['status'] in ['initialized', 'processing']
