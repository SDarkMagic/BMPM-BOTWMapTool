import pathlib
import os
import json
import oead
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
    if dirToLoop.is_file():
        subDir = dirToLoop
        if ((str(subDir).split('.'))[-1] == 'smubin' or (str(subDir).split('.'))[-1] == 'mubin'):
                fileList.append(subDir)
        else:
            print('File entered was not a proper map file.')
    else:
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

# Function for loading the actor parameter database when necessary
def loadActorDatabase():
    dataPath = data_dir()
    jsonFile = dataPath / 'actorParamDatabase.json'
    if (jsonFile.exists() == True):
        openFile = open(jsonFile, 'rt')
        paramDB = json.loads(openFile.read())
    else:
        print('The actor parameter database could not be found. Please create one by running "bmpm genDB" followed by where the map files from your game dump are stored.')
    return(paramDB)

# a function for scanning and modifying a dicitonaries contents to fit with the byml format
def dictParamsToByml(dictIn):
    subDict = {}
    dictOut = {}
#    print(dictIn)
    for key in dictIn.keys():
        keyVal = dictIn.get(key)
        if isinstance(keyVal, int):
            dictOut.update({key: oead.S32(keyVal)})
        elif isinstance(keyVal, dict):
            subDict.update({key: keyVal})
            dictOut.update({key: dictParamsToByml(subDict)})
        elif isinstance(keyVal, str):
            dictOut.update({key: keyVal})
        elif isinstance(keyVal, float):
            dictOut.update({key: oead.F32(keyVal)})
        elif keyVal == None:
            dictOut.update({key: 'none'})
        else:
            print('error?')
            dictOut.update({key: keyVal})
#    print(dictOut)
    return(((dict(dictOut))))
    