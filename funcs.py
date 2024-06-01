
import platform

def copy(src, dst):
    data = bytearray(1024)
    while (dataLen := src.readinto(data)) != 0:
        dst.write(memoryview(data)[:dataLen])


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
