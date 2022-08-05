from datetime import datetime

from core.camunda import start_process
from core.models import Profile

PROCESS_ID = 'Process_0rlunnd'


def start_cm(responsible: str, task_name: str, telegram_id: str, perform_before: str = '') -> tuple:
    """Start cm process in Camunda"""
    variables = {
        "task_restriction": {"value": perform_before, "type": "Date"},
        "performer": {"value": responsible, "type": "String"},
        "task_name": {"value": task_name, "type": "String"},
        "initiator_telegram": {"value": telegram_id, "type": "String"}
        }
    business_key = f'{datetime.now()} cm'
    status, response = start_process(PROCESS_ID, variables, business_key)
    return status, response
