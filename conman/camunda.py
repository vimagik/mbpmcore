from datetime import datetime

from core.camunda import start_process

PROCESS_ID = 'Process_0rlunnd'


def start_cm(responsible: str, perform_before: datetime = '') -> tuple:
    variables = {
        "task_restriction": {"value": perform_before, "type": "Date"},
        "performer": {"value": responsible, "type": "String"},
        }
    business_key = f'{datetime.now()} cm'
    status, response = start_process(PROCESS_ID, variables, business_key)
    return status, response
