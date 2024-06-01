#!/usr/bin/env python3

import sys, os, platform, configparser, requests
sys.path.insert(0, os.path.abspath(".."))
from funcs import OsType
import funcs


class Config:
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read("network.ini")
        self.url = parser["Config"]["URL"] + "/"
        self.username = parser["Config"]["Username"]
        self.password = parser["Config"]["Password"]
CONFIG = Config()


class Download:
    def __init__(self):
        self.url = CONFIG.url + "files/"
        self.username = CONFIG.username
        self.os = funcs.OS_TYPE
        self.arch = funcs.ARCH_TYPE

    def _buildOsName(self):
        return self.os.NAME + "-" + self.arch.NAME + self.os.EXE_SUFFIX

    def downloadExecutables(self):
        self.downloadTo("restic-" + self._buildOsName(), "restic.exe")
        self.downloadTo("resticprofile-" + self._buildOsName(), "resticprofile.exe")

    def downloadConfigs(self):
        self.downloadTo("conf-mail.tpl", "conf-mail.tpl")
        self.downloadTo("conf-all.yaml", "conf-all.yaml")
        self.downloadTo("conf-" + self.os.NAME + ".yaml", "conf-os.yaml")
        self.downloadTo("conf-" + self.username + ".yaml", "profiles.yaml", isPublic=False)

    def downloadTo(self, file, targetName, isPublic=True):
        url = self.url + (isPublic and "public/" or "private/") + file
        with requests.get(url, auth=(CONFIG.username, CONFIG.password), headers={"Accept-Encoding": None},
                          timeout=60, verify="server.crt", stream=True) as response, open(targetName, mode="wb") as target:
            response.raise_for_status()
            funcs.copy(response.raw, target)


dl = Download()
dl.downloadExecutables()
dl.downloadConfigs()
