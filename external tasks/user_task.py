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


def user_task(task: ExternalTask):
    user = task.get_business_key()
    print(user)
    return task.complete()


if __name__ == '__main__':
    ExternalTaskWorker(worker_id='1').subscribe('user_task', user_task)
