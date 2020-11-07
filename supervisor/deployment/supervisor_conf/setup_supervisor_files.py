import os


env_str = ",".join(["{key}='{var}'".format(key=k, var=v) for k, v in os.environ.items()])
for filename in os.listdir(os.path.join(os.path.dirname(__file__))):
    if not filename.endswith(".conf"):
        continue
    with open(filename) as f:
        f = f.read().replace("{{env_string}}", env_str)
    print(f)
    print("*******************************************")
