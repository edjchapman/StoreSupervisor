from celery import shared_task

from stores.models import StoreFrontStatusLog, Store, StoreFront
from stores.services.store_statuses import store_online


@shared_task
def update_store_statuses():
    for store in Store.objects.all():
        if not store.is_open():
            continue
        for sf in store.storefront_set.filter(status=StoreFront.ACTIVE):
            StoreFrontStatusLog.objects.create(
                store_front=sf,
                online=store_online(sf)
            )
