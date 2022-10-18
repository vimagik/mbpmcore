from datetime import datetime
from typing import Optional
from django.contrib.auth.models import User

from core.camunda import start_process
from core.models import ProcessModel, ProcessInstanceModel
from conman.models import CmProcessContext

from directories.models import Meeting

PROCESS_ID = 'Process_0rlunnd'
PROCESS_CODE = 'cm'


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


def create_instance(short_name: str, what_to_do: str, perform_before: datetime, responsible: str, initiator: User, meeting: Optional[Meeting] = None) -> tuple:
    process_status = 'Планирование'
    if perform_before:
        perform_before_iso = perform_before.isoformat()[:19] + '.000UTC'
        process_status = 'Выполнение'
    else:
        perform_before_iso = perform_before
    initiator_telegram_id = initiator.profile.telegram_id
    status_code, camunda_response = start_cm(
        responsible,
        short_name,
        initiator_telegram_id,
        perform_before=perform_before_iso
    )
    if not status_code:
        return False, camunda_response

    responsible_user = User.objects.get(username__exact=responsible)
    process_context = CmProcessContext.objects.create(
        short_name=short_name,
        what_to_do=what_to_do,
        perform_before=perform_before,
        responsible=responsible_user
    )
    
    process_context.initiator = initiator
    process_context.camunda_instance_id = camunda_response.get('id')
    process_context.status = process_status
    if meeting:
        process_context.meeting = meeting
    process_context.save()

    process = ProcessModel.objects.get(code__exact=PROCESS_CODE)
    ProcessInstanceModel.objects.create(
        camunda_instance_id=camunda_response.get('id'),
        process=process,
    )
    return True, 'Instanse created'
