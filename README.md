Store Supervisor
================
Monitors the status of online storefronts on sites like Uber Eats and Deliveroo.

- Issue alerts when stores are offline.
- Stores a record of when stores are online/offline in order to provide periodic reports of store performance.

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

## Deployment

1. Setup and secure the VM

Set up a Debian-based VM at your chosen hosting provider.

```shell
# Setup non-root user to run Django
adduser supervisor
usermod -aG sudo supervisor # Give the user sudo privileges
exit

# Restrict access to server to just by SSH key
ssh-copy-id supervisor@<server-address> # Copies your public key to the non-root user profile on the VM
ssh supervisor@<server-address>
sudo nano /etc/ssh/sshd_config
# Uncomment and change the line that says "# Password Authentication yes" so that it reads "PasswordAuthentication no"

# Setup a firewall and allow SSH
sudo apt install ufw
sudo ufw allow OpenSSH
sudo ufw enable
```

2. Set the environment variables for the user
```shell
# /home/supervisor/.profile
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="<server-address>"
export APP_SETTINGS_ENV="PRODUCTION"
export DJANGO_SECRET_KEY="secret_key"

export DJANGO_DEFAULT_DB_ENGINE="django.db.backends.postgresql"
export DJANGO_DEFAULT_DB_NAME="db_name"
export DJANGO_DEFAULT_DB_HOST="localhost"
export DJANGO_DEFAULT_DB_PORT="5432"
export DJANGO_DEFAULT_DB_USER="username"
export DJANGO_DEFAULT_DB_PASSWORD="password"

export EMAIL_HOST_USER="<email-server-address>"
export EMAIL_HOST_PASSWORD="<email-host-password>"

```

3. Install the requirements
```shell
apt-get install python3-venv supervisor git
```

4. Checkout the repo on the server
```shell
cd /home/supervisor
git clone https://github.com/edjchapman/StoreSupervisor.git
```

5. Setup the Django environment

```shell
# Install Gunicorn into Python virtual environment
python3 -m venv /home/supervisor/venv
source /home/supervisor/venv/bin/activate
pip install -r /home/supervisor/StoreSupervisor/supervisor/requirements.txt
```

6. Setup Nginx
```shell
# Install requirements
apt install nginx

# Open config file for editing and replace what's there with the config below
nano /etc/nginx/sites-available/default

# Symlink the file to sites-enabled to activate it
ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Restart NGINX to activate
service nginx restart
```
Nginx config
```nginx
upstream store-supervisor-backend {
    server localhost:8000;
}

server {

    server_name <server-address>;

    ## Only requests to our Host are allowed i.e. natooraapp.uk.natoora.com
    if ($host !~* ^(<server-address>)$ ) {
        return 444;
    }

    keepalive_timeout 5;
    client_max_body_size 4G;

    error_log  /var/log/nginx/error.log warn;
    access_log  /var/log/nginx/access.log;

    location /media {
        alias /home/supervisor/media;
    }

    location /static {
        alias /home/supervisor/static;
    }

    location /static/admin {
        alias /home/supervisor/venv/lib/python3.7/site-packages/django/contrib/admin/static/admin;
    }

    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {

        proxy_pass http://store-supervisor-backend;

        # Sets the HTTP protocol version for proxying. By default, version 1.0 is used.
        # Version 1.1 is recommended for use with keepalive connections and NTLM authentication.
        proxy_http_version 1.1;

        # WebSocket support. Depending on the request value, set the Upgrade and connection headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # We've set the host header, so we don't need Nginx to muddle about with redirects
        proxy_redirect off;

        # pass the Host: header from the client for the sake of redirects
        proxy_set_header  Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Host $server_name;

        # proxy_buffering off for proxying to websockets
        proxy_buffering off;

        # enable this if you use HTTPS:
        proxy_set_header X-Forwarded-Proto https;

        proxy_set_header content-type "application/json";

    }



    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/<server-address>/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/<server-address>/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {

    server_name _; # Catchall value for any attempt to  which will never trigger on a real hostname.

    access_log /var/log/nginx/catchall-access.log;

    return 444;

}


server {
    if ($host = <server-address>) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    server_name <server-address>;
    listen 80;
    return 404; # managed by Certbot
}
```

7. Deploying updates

The script `supervisor/deploy.py` should handle future updates.

Set the variables in the script and run it
```shell
python3 supervisor/deploy.py
```

---

## Celery Configuration
Celery runs period tasks (e.g. issuing emails etc)

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

#### Local development
```
celery -A supervisor beat -l info
celery -A supervisor worker -l info -E
```

#### Production configuration with Supervisor

```
# /etc/supervisor/conf.d/celery_worker.conf
; ==================================
;  celery worker supervisor example
; ==================================

; the name of your supervisord program
[program:supervisor_celery_worker]

; Set full path to celery program if using virtualenv
command=/home/supervisor/venv/bin/celery worker -A supervisor --loglevel=INFO

; The directory to your Django project
directory=/home/supervisor/StoreSupervisor

; If supervisord is run as the root user, switch users to this UNIX user account
; before doing any processing.
user=supervisor

; Supervisor will start as many instances of this program as named by numprocs
numprocs=1

; Put process stdout output in this file
stdout_logfile=/home/supervisor/logs/celery/celery_worker.log

; Put process stderr output in this file
stderr_logfile=/home/supervisor/logs/celery/celery_worker.log

; If true, this program will start automatically when supervisord is started
autostart=true

; May be one of false, unexpected, or true. If false, the process will never
; be autorestarted. If unexpected, the process will be restart when the program
; exits with an exit code that is not one of the exit codes associated with this
; process’ configuration (see exitcodes). If true, the process will be
; unconditionally restarted when it exits, without regard to its exit code.
autorestart=true

; The total number of seconds which the program needs to stay running after
; a startup to consider the start successful.
startsecs=10

; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if your broker is supervised, set its priority higher
; so it starts first
priority=998
Celery Scheduler: supervisor_celerybeat.conf
```


#### Reload Supervisor config
```
$ sudo supervisorctl reread
$ sudo supervisorctl update
```
