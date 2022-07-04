import requests

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


def send_to_telegram(task_name: str, status: str):
    text_message = f'Процесс "Непрерывный менеджмент"\nЗадача "{task_name}"\nСтатус - {status}'
    bot_url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    user_id = 129951811
    json_data = {
        'chat_id': user_id,
        'text': text_message,
    }
    requests.post(bot_url, data=json_data)


def send_to_telegram_task(task: ExternalTask) -> TaskResult:
    task_name = task.get_variable('task_name')
    send_to_telegram(
        task_name=task_name,
        status='Перенос срока'
    )
    return task.complete()


if __name__ == '__main__':
    ExternalTaskWorker(worker_id='1').subscribe('cm_send_to_telegram', send_to_telegram_task)
