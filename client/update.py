#!/usr/bin/env python3

import io, configparser, requests, subprocess, traceback
from funcs import OsType
import funcs


class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read("network.ini")
        self.url = parser["Config"]["URL"] + "/"
        self.username = parser["Config"]["Username"]
        self.password = parser["Config"]["Password"]
        self.ssl = parser["Config"]["SSL"]
        if self.ssl.lower() == "true":
            self.ssl = True
        elif self.ssl.lower() == "false":
            self.ssl = False


class Download:
    def __init__(self):
        self.url = CONFIG.url + "files/"
        self.username = CONFIG.username
        self.os = funcs.OS_TYPE
        self.arch = funcs.ARCH_TYPE

    def downloadConfigs(self):
        self.downloadTo("conf-all.toml", "conf-all.toml")
        self.downloadTo("conf-" + self.os.NAME + ".toml", "conf-os.toml")
        self.downloadTo("conf-" + self.username + ".toml", "profiles.toml", isPublic=False)

    def downloadTo(self, file, targetName, isPublic=True):
        url = self.url + (isPublic and "public/" or "private/") + file
        with requests.get(url, auth=(CONFIG.username, CONFIG.password), headers={"Accept-Encoding": None},
                          timeout=60, verify=CONFIG.ssl, stream=True) as response, open(targetName, mode="wb") as target:
            response.raise_for_status()
            funcs.copy(response.raw, target)
            log("Downloaded", file, "to", targetName)


class Schedules:
    def __init__(self):
        self.os = funcs.OS_TYPE

    def unschedule(self):
        log("Unschedule")
        log(runProcess("resticprofile" + self.os.EXE_SUFFIX, "unschedule", "--all"))

    def schedule(self):
        log("Schedule")
        log(runProcess("resticprofile" + self.os.EXE_SUFFIX, "schedule", "--all"))


def runProcess(*cmdLine):
    result = subprocess.run(cmdLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != 0:
        log("Cant run", cmdLine, "Output:", result.stdout)
        result.check_returncode()
    return result.stdout


def doUpdates():
    os = funcs.OS_TYPE
    log("Run restic self-update")
    log(runProcess("restic" + os.EXE_SUFFIX, "self-update"))
    log()
    log("Run resticprofile self-update")
    log(runProcess("resticprofile" + os.EXE_SUFFIX, "self-update"))
    log()


OUT = io.StringIO()
def log(*args):
        print(*args)
        print(*args, file=OUT)


def main():
    try:
        schedules = Schedules()
        schedules.unschedule()

        doUpdates()
        Download().downloadConfigs()

        schedules.schedule()
    except:
        traceback.print_exc(file=OUT)
        traceback.print_exc()
    funcs.sendMail(CONFIG.url + "sendMail.py", (CONFIG.username, CONFIG.password), CONFIG.ssl, "Update", OUT.getvalue())

CONFIG = Config()

main()
