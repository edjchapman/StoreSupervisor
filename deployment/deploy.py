from fabric import Connection

SERVER_HOST_NAME = "<SERVER-HOST-NAME>"
SERVER_USER = "supervisor"
PUBLIC_KEY_PATH = "/Users/YOUR_USER_HERE/.ssh/id_rsa.pub"

c = Connection(
    host=SERVER_HOST_NAME,
    user=SERVER_USER,
    connect_kwargs={
        "key_filename": PUBLIC_KEY_PATH
    }
)

# Update Repo
with c.cd('/home/supervisor/StoreSupervisor'):
    c.run('git pull origin master')
    c.run('git reset --hard origin/master')

# Setup Supervisor files
deployment_path = "/home/supervisor/StoreSupervisor/supervisor/deployment/"

with c.cd('/home/supervisor/StoreSupervisor'):
    c.run('source ~/.profile; /home/supervisor/vsuper/bin/python {}/supervisor_conf/setup_supervisor_files.py'.format(
        deployment_path
    ))

# Copy supervisor files to supervisor path
c.sudo('cp {}/supervisor_conf/daphne.conf /etc/supervisor/conf.d/daphne.conf'.format(deployment_path))
c.sudo('cp {}/supervisor_conf/celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf'.format(deployment_path))
c.sudo('cp {}/supervisor_conf/celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf'.format(deployment_path))

# Update supervisor
c.sudo('supervisorctl reread')
c.sudo('supervisorctl update')
c.sudo('supervisorctl start all')

# Copy NGINX conf to NGINX path
c.sudo('cp {}/nginx_conf/conf.nginx /etc/nginx/sites-available/store-supervisor'.format(deployment_path))
c.sudo('ln -sf /etc/nginx/sites-available/store-supervisor /etc/nginx/sites-enabled/store-supervisor')
c.sudo('nginx -s reload')
