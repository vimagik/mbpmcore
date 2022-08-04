from datetime import datetime

from core.camunda import start_process
from core.models import Profile

PROCESS_ID = 'Process_0rlunnd'


def start_cm(responsible: str, task_name: str, perform_before: str = '') -> tuple:
    """Start cm process in Camunda"""
    responsible_profile = Profile.objects.get(user__username__exact=responsible)
    if not responsible_profile:
        return False, {'error': 'An error in the profile of the person responsible'}
    variables = {
        "task_restriction": {"value": perform_before, "type": "Date"},
        "performer": {"value": responsible, "type": "String"},
        "task_name": {"value": task_name, "type": "String"},
        "performer_telegram": {"value": responsible_profile.telegram_id, "type": "String"}
        }
    business_key = f'{datetime.now()} cm'
    status, response = start_process(PROCESS_ID, variables, business_key)
    return status, response
