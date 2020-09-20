from celery import shared_task
from stores.models import StoreFrontStatusLog

@shared_task
def update_store_statuses():
    print("Hi")
