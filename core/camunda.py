from django.contrib.auth.models import User
import requests
import time

BASE_URL = 'http://localhost:8080/engine-rest/'
MAX_RETRIES = 5


def send_post_camunda_request(url: str, data: dict) -> tuple:
    """Wrap for post request in Camunda"""
    attempt_num = 0
    while attempt_num < MAX_RETRIES:
        r = requests.post(url, json=data)
        if r.status_code in [200, 204]:
            if r.text:
                return True, r.json()
            else:
                return True, ''
        else:
            attempt_num += 1
            time.sleep(2)
    return False, {'error': 'Camunda not available'}


def get_all_user_task(user: User) -> tuple:
    """Get list tasks of current user"""
    url = BASE_URL + 'task'
    groups = []
    for value in user.groups.all():
        groups.append(value.name)
    if len(groups) == 0:
        data = {
        'orQueries': [
            {
                'assignee': user.username,
            }
        ]
    }
    else:
        data = {
            'orQueries': [
                {
                    'candidateGroups': groups,
                    'assignee': user.username,
                }
            ]
        }
    return send_post_camunda_request(url, data)


def start_process(process_id: str, variables: dict, business_key: str) -> tuple:
    """Start a new process in camunda"""
    url = f'{BASE_URL}process-definition/key/{process_id}/start'
    data = {
        'businessKey': business_key,
        'variables': variables,
    }
    return send_post_camunda_request(url, data)


def complete_task(task_id: str, variables: dict) -> tuple:
    """Start a new process in camunda"""
    url = f'{BASE_URL}task/{task_id}/complete'
    data = {
        'variables': variables,
    }
    return send_post_camunda_request(url, data)

