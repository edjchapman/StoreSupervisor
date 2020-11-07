import os

file_path = os.path.join(os.path.dirname(__file__), "daphne.conf")
env_str = ",".join(["{key}='{var}'".format(key=k, var=v) for k, v in os.environ.items()])
with open(file_path) as f:
    f = f.read().replace("{{env_string}}", env_str)
print(f)
