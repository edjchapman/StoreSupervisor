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

with c.cd('/home/supervisor/Supervisor'):
    c.run('git pull origin master')
    c.run('git reset --hard origin/master')
    c.run('/home/supervisor/vsuper/bin/python supervisor/deployment/daphne/setup_daphne.py')
