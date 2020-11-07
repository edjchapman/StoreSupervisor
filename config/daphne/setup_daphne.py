import multiprocessing
import os
import subprocess


class SetupDaphne:
    """
    Set up Daphne to run Store Supervisor with web sockets.

    Can run for initial set up or repeatedly for updates.
    """

    def __init__(self):
        self.install()
        self.write_conf_file()

    @staticmethod
    def install():
        """
        Install supervisor and create dir for daphne sock files to run in.
        """
        subprocess.call("apt-get -y update", shell=True)
        subprocess.call("apt-get install -y supervisor", shell=True)
        os.makedirs("/run/daphne", exist_ok=True)

    def write_conf_file(self):
        """
        Write daphne conf data to file.
        """
        with open("/etc/supervisor/conf.d/daphne.conf", "w") as conf:
            conf.write("[fcgi-program:asgi]\n")
            conf.write("socket=tcp://0.0.0.0:8000\n")
            conf.write("directory=/home/supervisor/Supervisor\n")
            conf.write(
                "command=/home/supervisor/vsuper/bin/daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers supervisor.asgi:application\n")
            conf.write("numprocs={}\n".format(self.get_numprocs()))
            conf.write("process_name=asgi%(process_num)d\n")
            conf.write("autostart=true\n")
            conf.write("autorestart=true\n")
            conf.write("stdout_logfile=/var/log/daphne.log\n")
            conf.write("redirect_stderr=true\n")
            # Generate string of all environment variables to put in the conf.
            # Supervisor doesn't spawn a shell so this is the only way so far.
            conf.write("environment={}\n".format(
                ",".join(["{key}='{var}'".format(
                    key=key,
                    var=self.remove_percentages(key, var)) for (key, var) in os.environ.items()]
                )
            ))

    @staticmethod
    def get_numprocs():
        numprocs = os.environ.get("DAPHNE_PROCESSES", multiprocessing.cpu_count())
        return int(numprocs or 0)

    @staticmethod
    def remove_percentages(key, var):
        """Replace '%' chars with '_' as they are a special character in supervisor.

        Output special TeamCity stdout message so that it gets flagged as a warning in the build if there is a % char.

        :param key: Environment variable key name.
        :param var: Environment variable var.
        :return: Var with '%' chars replaced with '_' chars if there are any.
        """
        if "%" in var:
            name = '% replaced with _ in environment variable {key} in daphne conf'.format(key=key)
            description = '% char cannot be used in supervisor conf file, so it has been replaced with an underscore.'
            category = 'Daphne Conf Violation'
            teamcity_warning = "##teamcity[inspectionType id='1' name={} description={} category={}]".format(
                name,
                description,
                category
            )
            subprocess.call("echo {teamcity_warning}".format(teamcity_warning=teamcity_warning), shell=True)
            var = var.replace("%", "_")
        return var
