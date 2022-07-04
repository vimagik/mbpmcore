from datetime import datetime

from core.camunda import start_process

PROCESS_ID = 'Process_0rlunnd'


def start_cm(responsible: str, task_name: str, perform_before: str = '') -> tuple:
    variables = {
        "task_restriction": {"value": perform_before, "type": "Date"},
        "performer": {"value": responsible, "type": "String"},
        "task_name": {"value": task_name, "type": "String"},
        }
    business_key = f'{datetime.now()} cm'
    status, response = start_process(PROCESS_ID, variables, business_key)
    return status, response
