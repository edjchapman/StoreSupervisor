import os

with open('beat.conf', 'w') as beatfile:
    beatfile.read()
        "<ENV>",
        ",".join(
            ["{key}={value}".format(key=key, value=value) for (key, value) in os.environ.items()]
        )


# import argparse
# import logging
# import os
# import shutil
# import subprocess
# import textwrap
#
# logger = logging.getLogger(__name__)
#
#
# class NginxConfiguration:
#     """
#     Set up NGINX configuration on Debian server.
#
#     Make edits to config in config_files/ws.nginx.
#
#     Can be used for initial set up, or run repeatedly for updates.
#     """
#
#     def __init__(self, host_name, ssl=False):
#         """
#         :param host_name: Server host name, passed as arg when running script.
#         :param ssl: Boolean, whether to setup HTTPS.
#         """
#         self.host_name = host_name
#         self.use_ssl = ssl
#
#     def setup(self):
#         """
#         Run methods to set up configuration file.
#         """
#         self.install()
#         nginx_conf = self.setup_config()
#         self.write_file(nginx_conf)
#         self.remove_default()
#         self.symlink()
#         if use_ssl:
#             self.setup_ssl_certificates()
#
#     def install(self):
#         """
#         Stop Apache (as it runs on port 80).  Install NGINX.
#         """
#         subprocess.call("apt-get -y update", shell=True)
#         subprocess.call("service apache2 stop", shell=True)
#         subprocess.call("apt-get -y install nginx", shell=True)
#
#     def setup_config(self):
#         """Open config file from repo and update parameters.
#
#         :return: Formatted NGINX config file.
#         """
#         path = os.path.join(os.path.dirname(__file__), "config_files", "ws.nginx")
#         with open(path) as nginx_conf:
#             nginx_conf = nginx_conf.read(
#             ).replace(
#                 "<host_name>", self.host_name
#             ).replace(
#                 "<listen_port>", "443 ssl http2" if self.use_ssl else "80"
#             ).replace(
#                 "<ssl_cert>", "ssl_certificate /etc/nginx/ssl/ssl-bundle.crt;" if self.use_ssl else ""
#             ).replace(
#                 "<ssl_key>", "ssl_certificate_key /etc/nginx/ssl/{}.key;".format(self.host_name) if self.use_ssl else ""
#             )
#         return nginx_conf
#
#     def write_file(self, nginx_conf):
#         """
#         Write NGINX config to sites-available file.
#         """
#         path = "/etc/nginx/sites-available/ws"
#         with open(path, "w") as nginx_conf_output:
#             if self.use_ssl:
#                 nginx_conf_output.write(textwrap.dedent(self.https_redirect()))
#             nginx_conf_output.write(textwrap.dedent(nginx_conf))
#
#     def remove_default(self):
#         """Remove default NGINX config file from sites-enabled if it exists.
#
#         We leave it in sites-available, as this is updated with NGINX with new examples.
#         """
#         if os.path.exists('/etc/nginx/sites-enabled/default'):
#             os.remove('/etc/nginx/sites-enabled/default')
#
#     def symlink(self):
#         """
#         Symlink WS NGINX conf file to sites-enabled to activate it.
#         """
#         try:
#             os.symlink('/etc/nginx/sites-available/ws', '/etc/nginx/sites-enabled/ws')
#         except OSError:
#             # Probably because it is already symlinked
#             pass
#
#     def setup_ssl_certificates(self):
#         """Set up NGINX to use SSL.
#
#         1. Make SSL directory.
#         2. Copy crt and key to SSL directory.
#         """
#         repo_ssl_dir = os.path.join(os.path.dirname(__file__), "ssl_files", self.host_name)
#         crt = os.path.join(repo_ssl_dir, "ssl-bundle.crt")
#         key = os.path.join(repo_ssl_dir, "{}.key".format(self.host_name))
#         server_ssl_dir = "/etc/nginx/ssl"
#         os.makedirs(server_ssl_dir, exist_ok=True)
#         shutil.copy2(src=crt, dst=server_ssl_dir)
#         shutil.copy2(src=key, dst=server_ssl_dir)
#
#     def https_redirect(self):
#         """Catch-all server block to redirect all traffic to port 80 to HTTPS.
#
#         :return: Server block.
#         """
#         block = """
#                 server {
#                     listen 80 default_server;
#                     server_name _; # Matches any hostname used
#                     return 301 https://$host$request_uri;
#                 }
#                 """
#         return block
#
#
# if __name__ == "__main__":
#     # Setup arguments
#     parser = argparse.ArgumentParser(description="Paramaters to setup NGINX config file.")
#     parser.add_argument('host_name')
#     parser.add_argument('--use_ssl', dest='use_ssl')
#
#     # Parse arguments
#     args = vars(parser.parse_args())
#     server_host_name = args.get('host_name', None)
#     use_ssl = args.get('use_ssl', "Yes")
#     use_ssl = True if use_ssl and "y" in use_ssl.lower() else False
#
#     # Run config setup
#     nginx_configuration = NginxConfiguration(host_name=server_host_name, ssl=use_ssl)
#     nginx_configuration.setup()
