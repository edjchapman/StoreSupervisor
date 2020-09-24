import requests

from stores.models import StoreFront


def deliveroo_store_online(url):
    r = requests.get(url)
    if "isn't currently accepting orders" in r.text:
        return False
    return True


def uber_eats_store_online(url):
    r = requests.get(url)
    if "Currently unavailable" in r.text:
        return False
    return True


def store_online(sf):
    if sf.platform == StoreFront.DELIVEROO:
        return deliveroo_store_online(sf.url)
    if sf.platform == StoreFront.UBER_EATS:
        return uber_eats_store_online(sf.url)
