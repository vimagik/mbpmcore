import requests
from datetime import datetime
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker

default_config = {
    'maxTask': 1,
    'lockDuration': 10000,
    'asyncResponseTimeout': 5000,
    'retries': 3,
    'retryTimeout': 5000,
    'sleepSeconds': 30,
}

API_TOKEN = '1033382685:AAEmbpKw8wg-Sbrx_xPsovKEQE2M2xEvRaY'


def send_to_telegram(task_name: str, message_type: str, due_date: datetime, telegram_id: str) -> None:
    if message_type == 'planDate':
        text_message = f'По задаче "{task_name}" установлен срок до {due_date.strftime("%d.%m.%Y")} включительно'
    elif message_type == 'postponeDate':
        text_message = f'По задаче "{task_name}" сдвинут срок до {due_date.strftime("%d.%m.%Y")} включительно'
    else:
        text_message = f'Задача "{task_name}" выполнена'
    bot_url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    json_data = {
        'chat_id': telegram_id,
        'text': text_message,
    }
    requests.post(bot_url, data=json_data)


def send_info(task: ExternalTask) -> TaskResult:
    task_name = task.get_variable('task_name')
    message_type = task.get_extension_property('type')
    due_date_str = task.get_variable('task_restriction')
    due_date = datetime.strptime(due_date_str[:19], "%Y-%m-%dT%H:%M:%S")
    telegram_id = task.get_variable('initiator_telegram')
    send_to_telegram(
        task_name=task_name,
        message_type=message_type,
        due_date=due_date,
        telegram_id=telegram_id
    )
    return task.complete()


if __name__ == '__main__':
    ExternalTaskWorker(worker_id='1').subscribe('cm_send_to_telegram', send_info)
