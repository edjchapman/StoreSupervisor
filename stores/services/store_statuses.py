import requests


def store_online(store_front):
    r = requests.get(store_front.url)
    if r.status_code == requests.codes.gone:
        return False
    if any(s in r.text.lower() for s in store_front.platform.search_texts()):
        return False
    return True
