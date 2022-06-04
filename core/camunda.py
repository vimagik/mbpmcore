from django.contrib.auth.models import User
import requests
import time

BASE_URL = 'http://localhost:8080/engine-rest/'
MAX_RETRIES = 5


def get_all_user_task(user: User):
    """Get list tasks of current user"""
    attempt_num = 0
    url = BASE_URL + 'task'
    groups = []
    for value in user.groups.all():
        groups.append(value.name)
    data = {
        'orQueries': [
            {
                'candidateGroups': groups,
                'assignee': user.username,
            }
        ]
    }
    while attempt_num < MAX_RETRIES:
        r = requests.post(url, json=data)
        if r.status_code == 200:
            return True, r.json()
        else:
            attempt_num += 1
            time.sleep(2)
    return False, {'error': 'Camunda not available'}
