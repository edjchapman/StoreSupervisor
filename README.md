Store Supervisor
================
Monitor the status of store fronts from a customer's perspective

## Celery

#### Local
```
celery -A supervisor beat -l info
celery -A supervisor worker -l info -E
```

#### Production

```
# /etc/supervisor/conf.d/celery_worker.conf
; ==================================
;  celery worker supervisor example
; ==================================

; the name of your supervisord program
[program:supervisor_celery_worker]

; Set full path to celery program if using virtualenv
command=/home/supervisor/vsuper/bin/celery worker -A supervisor --loglevel=INFO

; The directory to your Django project
directory=/home/supervisor/Supervisor

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


```
# /etc/supervisor/conf.d/celery_beat.conf
; ================================
;  celery beat supervisor example
; ================================

; the name of your supervisord program
[program:supervisor_celery_beat]

; Set full path to celery program if using virtualenv
command=/home/supervisor/vsuper/bin/celery -A supervisor --loglevel=INFO

; The directory to your Django project
directory=/home/supervisor/Supervisor

; If supervisord is run as the root user, switch users to this UNIX user account
; before doing any processing.
user=supervisor

; Supervisor will start as many instances of this program as named by numprocs
numprocs=1

; Put process stdout output in this file
stdout_logfile=/home/supervisor/logs/celery/celery_beat.log

; Put process stderr output in this file
stderr_logfile=/home/supervisor/logs/celery/celery_beat.log

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

; if your broker is supervised, set its priority higher
; so it starts first
priority=999
```

We also need to create the log files that are mentioned in the above scripts on the remote server:
```
$ touch /var/log/celery/picha_worker.log
$ touch /var/log/celery/picha_beat.log
```

Finally, run the following commands to make Supervisor aware of the programs - e.g., pichacelery and pichacelerybeat:
```
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

Run the following commands to stop, start, and/or check the status of the pichacelery program:
```
$ sudo supervisorctl stop pichacelery
$ sudo supervisorctl start pichacelery
$ sudo supervisorctl status pichacelery
```
