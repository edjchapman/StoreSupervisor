import requests


def store_online(store_front):
    r = requests.get(store_front.url)
    if store_front.platform.offline_search_text in r.text:
        return False
    return True
