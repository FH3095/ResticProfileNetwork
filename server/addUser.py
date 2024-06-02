#!/usr/bin/env python3

import sys, json, secrets
from pathlib import Path

sys.argv = ["a.py", "t3"]

ENCODING = "ascii"
PASSWORD_BYTES = 24 # should be divisible by 3
DEFAULT_CONFIG = """
version: "1"

includes:
    - "conf-all.yaml"
    - "conf-os.yaml"

default:
    inherit: conf-os
    repository: "rest:http://{Username}:{Password}@backup.host.example:8000/{Username}/main"
"""

if len(sys.argv) < 2:
    print("Missing username parameter", file=sys.stderr)
    sys.exit(1)

def writeJson(username, password):
    users = None
    with open("files/users.json", mode="rt", encoding=ENCODING) as file:
        users = json.load(file)
    users[username] = password
    with open("files/users.json", mode="wt", encoding=ENCODING) as file:
        json.dump(users, file, indent="\t")

def writeDefaultConfig(username, password):
    confFile = Path.cwd().joinpath("files", "private", "conf-" + username + ".yaml")
    if confFile.is_file():
        raise RuntimeError("User-Config " + str(confFile) + " already exists")
    confFile.parent.mkdir(parents=False, exist_ok=True)
    with open(confFile, mode="wt", encoding=ENCODING) as file:
        file.write(DEFAULT_CONFIG.format(Username=username, Password=password))

username = sys.argv[1]
password = secrets.token_urlsafe(PASSWORD_BYTES)

writeDefaultConfig(username, password)
writeJson(username, password)
