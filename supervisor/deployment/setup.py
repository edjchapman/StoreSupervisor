from fabric import Connection
import os
import textwrap

c = Connection(
    host='store-supervisor.website',
    user='supervisor',
    connect_kwargs={
        "key_filename": "/Users/ed/.ssh/id_rsa.pub"
    }
)

# Update Repo
with c.cd('/home/supervisor/Supervisor'):
    c.run('git pull origin master')
    c.run('git reset --hard origin/master')

# Setup Supervisor files
with c.cd('/home/supervisor/Supervisor'):
    c.run('source ~/.profile; /home/supervisor/vsuper/bin/python supervisor/deployment/supervisor_conf/setup_supervisor_files.py')

c.sudo('cp /home/supervisor/Supervisor/supervisor/deployment/supervisor_conf/daphne.conf /etc/supervisor/conf.d/daphne.conf')
c.sudo('cp /home/supervisor/Supervisor/supervisor/deployment/supervisor_conf/celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf')
c.sudo('cp /home/supervisor/Supervisor/supervisor/deployment/supervisor_conf/celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf')

c.sudo('supervisorctl reread')
c.sudo('supervisorctl update')
c.sudo('supervisorctl start all')
