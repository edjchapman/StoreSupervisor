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

# Setup Daphne
with c.cd('/home/supervisor/Supervisor'):
    c.run('source ~/.profile; /home/supervisor/vsuper/bin/python supervisor/deployment/daphne/setup_supervisor_files.py')

# c.sudo('cp /home/supervisor/Supervisor/supervisor/deployment/daphne/daphne.conf /etc/supervisor/conf.d/supervisor1.conf')
