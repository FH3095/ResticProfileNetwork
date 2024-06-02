#!/usr/bin/env python3

import sys, os, re, urllib.parse, requests, json, tempfile, shutil, bz2
from pathlib import Path
import funcs
funcs.gotoServerDir()


RESTIC_JSON_URL = "https://api.github.com/repos/restic/restic/releases/latest"
RESTICPROFILE_JSON_URL = "https://api.github.com/repos/creativeprojects/resticprofile/releases/latest"
DL_MATRIX = [(funcs.OsType.LINUX, funcs.ArchType.AMD64), (funcs.OsType.LINUX, funcs.ArchType.ARM64), (funcs.OsType.WINDOWS, funcs.ArchType.AMD64)]

class BinaryDl:
    def __init__(self, url, exeName, osType, archType):
        self.url = url
        self.exeName = exeName
        self.osType = osType
        self.archType = archType

    def getJson(self):
        with requests.get(self.url, timeout=30) as jsonRequest:
            jsonRequest.raise_for_status()
            return json.loads(jsonRequest.text)

    def findFullWord(self, toFind, string):
        toFind = re.escape(toFind)
        match = re.search(r"(?:^|[^a-zA-Z0-9])" + toFind + r"(?:$|[^a-zA-Z0-9])", string)
        return match != None

    def getFileUrl(self):
        json = self.getJson()["assets"]
        for dl in json:
            name = dl["name"]
            if self.findFullWord(self.exeName, name) and self.findFullWord(self.osType, name) and self.findFullWord(self.archType, name):
                return dl["browser_download_url"]
        return None

    def unzip(self, tempFile, targetFile):
        tempDir = Path(tempFile).parent

        if tempFile.endswith(".bz2") and not tempFile.endswith(".tar.bz2"):
            with bz2.open(tempFile, mode="rb") as src, open(targetFile, mode="wb") as dst:
                funcs.copy(src, dst)
                return

        shutil.unpack_archive(tempFile, tempDir)
        Path(tempFile).unlink()
        files = list(tempDir.glob(self.exeName + "*"))
        if len(files) != 1:
            raise RuntimeError("Too many or no files with "  + self.exeName + " in " + str(tempDir))
        shutil.copyfile(files[0], targetFile)


    def downloadFile(self, targetFile):
        dlUrl = self.getFileUrl()
        if dlUrl == None:
            raise RuntimeError("Cant find download-url for " + self.exeName + "-" + self.osType + "-" + self.archType)
        print("Found executable", self.exeName + "-" + self.osType + "-" + self.archType, "with url", dlUrl)
        dlFilename = urllib.parse.urlparse(dlUrl).path
        dlFilename = dlFilename[dlFilename.rindex("/")+1:]
        with tempfile.TemporaryDirectory() as directory:
            tempFile = os.path.join(directory, dlFilename)
            with open(tempFile, mode="wb") as dlFile, requests.get(dlUrl, timeout=30, stream=True) as dlRequest:
                funcs.copy(dlRequest.raw, dlFile)
            self.unzip(tempFile, targetFile)


Path.cwd().joinpath("files", "public").mkdir(parents=True, exist_ok=True)
for osType, archType in DL_MATRIX:
    dl = BinaryDl(RESTIC_JSON_URL, "restic", osType.RESTIC_NAME, archType.RESTIC_NAME)
    dl.downloadFile("files/public/restic-" + osType.NAME + "-" + archType.NAME + osType.EXE_SUFFIX)
    dl = BinaryDl(RESTICPROFILE_JSON_URL, "resticprofile", osType.RESTIC_PROFILE_NAME, archType.RESTIC_PROFILE_NAME)
    dl.downloadFile("files/public/resticprofile-" + osType.NAME + "-" + archType.NAME + osType.EXE_SUFFIX)
