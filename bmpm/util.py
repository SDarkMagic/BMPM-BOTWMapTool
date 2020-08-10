import pathlib
import os
from platform import system

def data_dir():
    if system() == "Windows":
        data_dir = pathlib.Path(os.path.expandvars("%LOCALAPPDATA%")) / "bmpm"
    else:
        data_dir = pathlib.Path.home() / ".config" / "bmpm"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    return(data_dir)

def checkDir(dirToLoop):
    fileList = []
    for subDir in dirToLoop.iterdir():
        if subDir.is_dir():
            checkDir(subDir)
        else:
            if ((str(subDir).split('.'))[-1] == 'smubin' or (str(subDir).split('.'))[-1] == 'mubin'):
                fileList.append(subDir)
                continue
            else:
                continue
    return(fileList)