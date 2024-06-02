
import platform, urllib.parse, requests, configparser

def copy(src, dst):
    data = bytearray(1024)
    while (dataLen := src.readinto(data)) != 0:
        dst.write(memoryview(data)[:dataLen])

def sendMail(url, auth, ssl, subject, text):
    url = url + "?" + urllib.parse.urlencode({"subject": subject})
    with requests.get(url, data=text, auth=auth, timeout=60, verify=ssl, stream=True) as response:
        response.raise_for_status()

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

class OsType:
    def __init__(self, name, exeSuffix, resticName, resticProfileName):
        self.NAME = name
        self.EXE_SUFFIX = exeSuffix
        self.RESTIC_NAME = resticName
        self.RESTIC_PROFILE_NAME = resticProfileName

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.NAME == other.NAME:
            return True
        else:
            return False

    def __str__(self):
        return "OsType<" + self.NAME + ">"

OsType.WINDOWS = OsType("win", ".exe", "windows", "windows")
OsType.LINUX = OsType("linux", "", "linux", "linux")
OsType.MAC = OsType("mac", "", "darwin", "darwin")


class ArchType:
    def __init__(self, name, resticName, resticProfileName):
        self.NAME = name
        self.RESTIC_NAME = resticName
        self.RESTIC_PROFILE_NAME = resticProfileName

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self.NAME == other.NAME:
            return True
        else:
            return False

    def __str__(self):
        return "ArchType<" + self.NAME + ">"

ArchType.AMD64 = ArchType("amd64", "amd64", "amd64")
ArchType.ARM64 = ArchType("arm64", "arm64", "arm64")


OS_TYPE = None
ARCH_TYPE = None

match platform.system().lower():
    case "windows":
        OS_TYPE = OsType.WINDOWS
    case "linux":
        OS_TYPE = OsType.LINUX
    case "darwin":
        OS_TYPE = OsType.MAC
    case _:
        raise RuntimeError("Unknown platform " + str(platform.system()))

match platform.machine().lower():
    case "amd64" | "x86_64":
        ARCH_TYPE = ArchType.AMD64
    case "arm64" | "aarch64":
        ARCH_TYPE = ArchType.ARM64
    case _:
        raise RuntimeError("Unknown architecture " + str(platform.machine()))
