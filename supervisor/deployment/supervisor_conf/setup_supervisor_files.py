import os


env_str = ",".join(["{key}='{var}'".format(key=k, var=v) for k, v in os.environ.items()])
directory = os.path.join(os.path.dirname(__file__))
for filename in os.listdir(directory):
    if not filename.endswith(".conf"):
        continue
    file_path = os.path.join(directory, filename)
    with open(file_path) as f:
        f = f.read()
    with open(file_path) as f_out:
        f_out.write(f.replace("{{env_string}}", env_str))
    print(f)
    print("*******************************************")
