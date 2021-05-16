Store Supervisor
================

Store Supervisor assists in the management of online stores, monitoring their online status.

The user can define the URL of the storefront (e.g. on Deliveroo or Uber Eats), and the text to determine whether the
store is online (e.g. “Currently Unavailable”).

If a store is offline when it shouldn’t be, the user to be contacted, so they can take action to maintain its online
presence.

The data is also stored and can be exported to a spreadsheet to provide periodic reports of storefronts’ uptime.


---

## Local Development

Clone the repo

```shell
git clone https://github.com/edjchapman/StoreSupervisor.git
```

Install project requirements
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r supervisor/requirements.txt
```

Run migrations
```shell
./manage.py migrate
```

Run server
```shell
./manage.py runserver
```

---

## Deployments

Instructions, config and deployment instructions can be found in the deployment directory.

---

## License

- Copyright © [Edward Chapman](https://edwardchapman.co.uk "Store Supervisor").
