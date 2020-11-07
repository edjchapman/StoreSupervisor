from fabric import Connection

c = Connection(
    host='store-supervisor.website',
    user='supervisor',
    connect_kwargs={
        "key_filename": "/Users/ed/.ssh/id_rsa.pub"
    }
)


def update_production_dir(c):
    with c.cd('/home/supervisor/Supervisor'):
        c.run('git pull origin master')
        c.run('git reset --hard origin/master')


def setup_daphne(c):
    c.run("python3 /home/supervisor/Supervisor/config/daphne/setup_daphne.py")
    c.sudo('supervisorctl reread')
    c.sudo('supervisorctl update')
    c.sudo('supervisorctl restart all')


update_production_dir(c)
setup_daphne(c)


"""
CONNECTION RESULTS

print(result.stdout.strip())
print(result.ok)
print(result.command)
print(result.connection)
print(result.connection.host)
"""


"""
PUT

def upload_and_unpack(c):

    c.put('manage.py', remote='/home/supervisor/testing')
    c.run('tar -C /opt/mydata -xzvf /opt/mydata/myfiles.tgz')
"""

"""
PROMPT FOR PASSWORD

import getpass
from fabric import Connection, Config

sudo_pass = getpass.getpass("What's your sudo password?")
config = Config(overrides={'sudo': {'password': sudo_pass}})
c = Connection('db1', config=config)
c.sudo('whoami', hide='stderr')
c.sudo('useradd mydbuser')
c.run('id -u mydbuser')
"""
