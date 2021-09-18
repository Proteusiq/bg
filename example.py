from os import environ
from celery.result import AsyncResult
from celery.app.task import Task

# from tasks import to_parquent, train

# hide this load as .env
environ["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
environ["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"


def run_task(func: Task, task_name: str, **kwargs):

    task = func.delay(**kwargs)

    return {"task_id": task.id, "task_name": task_name}


def get_results(task_id: str):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return result


# if __name__ == "__main__":

#     import pandas as pd

#     data = pd.DataFrame({"agents": ["James Bond", "Jason Bourne"]}).to_dict(
#         orient="records"
#     )

#     r = run_task(
#         func=to_parquent, task_name="to_parquent", data=data, snooze=10
#     )  # pretend

#     d = run_task(func=train)
#     task_id = r.get("task_id")
#     status = get_results(task_id)
