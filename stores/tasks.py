from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from stores.models import StoreFrontStatusLog


@periodic_task(run_every=(crontab()), name="update_store_statuses", ignore_result=True)
def update_store_statuses():
    print("Hi")
