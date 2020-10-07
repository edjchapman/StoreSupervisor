import time

from celery import shared_task

from stores.emails import offline_stores_report_email
from stores.models import StoreAudit, Store, StoreFront
from stores.services.store_statuses import store_online


@shared_task
def update_store_statuses():
    offline_stores = []
    for store in Store.objects.all():
        if store.open_today() and store.open_now():
            for sf in store.storefront_set.filter(status=StoreFront.ACTIVE):
                is_online = store_online(sf)
                time.sleep(1)
                StoreAudit.objects.create(
                    store_front=sf,
                    online=is_online
                )
                if not is_online:
                    offline_stores.append(sf)
    offline_stores_report_email(offline_stores)
