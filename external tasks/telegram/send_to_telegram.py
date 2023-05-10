import requests
import os
from datetime import datetime
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker


API_TOKEN = "1033382685:AAEmbpKw8wg-Sbrx_xPsovKEQE2M2xEvRaY"
CAMUNDA_HOST = os.environ.get("CAMUNDA_HOST", "localhost")
BASE_CAMUNDA_URL = f"http://{CAMUNDA_HOST}:8080/engine-rest"
CAMUNDA_USER=os.environ.get("CAMUNDA_USER", "demo")
CAMUNDA_API_PASSWORD=os.environ.get("CAMUNDA_API_PASSWORD", "demo")

default_config = {
    "auth_basic": {"username": CAMUNDA_USER, "password": CAMUNDA_API_PASSWORD},
    "maxTask": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30,
}


def send_to_telegram(
    task_name: str, message_type: str, due_date: datetime, telegram_id: str
) -> None:
    """Sending a telegram message for the CM process"""
    if message_type == "planDate":
        text_message = f'По задаче "{task_name}" установлен срок до {due_date.strftime("%d.%m.%Y")} включительно'
    elif message_type == "postponeDate":
        text_message = f'По задаче "{task_name}" сдвинут срок до {due_date.strftime("%d.%m.%Y")} включительно'
    else:
        text_message = f'Задача "{task_name}" выполнена'
    bot_url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    json_data = {
        "chat_id": telegram_id,
        "text": text_message,
    }
    requests.post(bot_url, data=json_data)


def send_info(task: ExternalTask) -> TaskResult:
    """External task Camunda shell"""
    task_name = task.get_variable("task_name")
    message_type = task.get_extension_property("type")
    due_date_str = task.get_variable("task_restriction")
    due_date = datetime.strptime(due_date_str[:19], "%Y-%m-%dT%H:%M:%S")
    telegram_id = task.get_variable("initiator_telegram")
    send_to_telegram(
        task_name=task_name,
        message_type=message_type,
        due_date=due_date,
        telegram_id=telegram_id,
    )
    return task.complete()


if __name__ == "__main__":
    ExternalTaskWorker(
        worker_id="1", config=default_config, base_url=BASE_CAMUNDA_URL
    ).subscribe("cm_send_to_telegram", send_info)
