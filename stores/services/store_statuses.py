import requests


def store_online(store_front):
    r = requests.get(store_front.url)
    return any(s in r.text.lower() for s in store_front.platform.search_texts())
