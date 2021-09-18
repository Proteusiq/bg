import pickle
from time import sleep
from typing import List
from decouple import config
from celery import Celery
import pandas as pd
from sklearn.pipeline import Pipeline

celery = Celery(__name__)

celery.conf.broker_url = config("CELERY_BROKER_URL")
celery.conf.result_backend = config("CELERY_RESULT_BACKEND")


@celery.task(name="train")
def train(
    model_path: str,
    pipeline_path: str,
    features: List[str],
    target: str,
    file_path: str = None,
) -> bytes:

    dataf = pd.read_parquet(file_path)
    X, y = dataf[features], dataf[target]

    # unpickle, train, then pickle again :)
    with open(f"{pipeline_path}", "rb") as f, open(f"{model_path}", "wb") as g:
        pipeline = pickle.load(f)

        pipeline.fit(X, y)

        pickle.dump(pipeline, g)

    return {"model_path": model_path}


@celery.task(name="to_parquet")
def to_parquent(data: dict, file_path: str = None, snooze: int = 60) -> dict:

    sleep(snooze)  # pretending to do heavy task
    if file_path is None:
        file_path = "data/example.parquet"
    dataf = pd.DataFrame.from_dict(data)
    dataf.to_parquet(file_path, index=False)

    return {"file_path": file_path, "snooze": snooze}
