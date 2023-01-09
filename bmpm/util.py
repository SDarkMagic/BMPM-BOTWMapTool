import pathlib
import os
import json
import oead
import byml
import yaml
import io
from platform import system

def compressByml(filePath, savePath, bigEndian, Version=2):
    loader = yaml.CSafeLoader
    byml.yaml_util.add_constructors(loader)
    with open(filePath, 'r', encoding='utf-8') as ymlData:
        yml = yaml.load(ymlData, Loader=loader)
        buf = io.BytesIO()
        byml.Writer(yml, be=bigEndian, version=Version).write(buf)
        buf.seek(0)

    with open(savePath, 'wb') as writeFile:
        writeFile.write(oead.yaz0.compress(buf.read()))
    return

def data_dir():
    if system() == "Windows":
        data_dir = pathlib.Path(os.path.expandvars("%LOCALAPPDATA%")) / "bmpm"
    else:
        data_dir = pathlib.Path.home() / ".config" / "bmpm"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    return(data_dir)

def checkDir(dirToLoop, acceptableExts: list):
    fileList = []
    if dirToLoop.is_file():
        subDir = dirToLoop
        if ((str(subDir).split('.'))[-1] in acceptableExts):
            fileList.append(subDir)
        else:
            print(f'File: {dirToLoop} entered was not a proper map file.')
    else:
        for subDir in dirToLoop.iterdir():
#            print(str(subDir).split('.')[-1])
            if subDir.is_dir():
                fileList.extend(checkDir(subDir, acceptableExts))
            else:
                if ((str(subDir).split('.'))[-1] in acceptableExts):
                    fileList.append(subDir)
                else:
                    print(f'File: {subDir} entered was not a proper map file.')
                    continue
#    print(fileList)
    return(fileList)
"""    if dirToLoop.is_file():
        subDir = dirToLoop
        if ((str(subDir).split('.'))[-1] == 'smubin' or (str(subDir).split('.'))[-1] == 'mubin'):
                fileList.append(subDir)
        else:
            print('File entered was not a proper map file.')
"""

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

# A function for checking if a file is yaz0 compressed and then determining whether or not to decompress it based off of that
def checkCompression(fileCheck):
    fileInRead = fileCheck
    if (oead.yaz0.get_header(fileInRead) is not None):
        print("File is Yaz0 compressed, decompressing")
        uncompressedFile = oead.yaz0.decompress(fileInRead)
    else:
        print('File is not compressed with Yaz0')
        uncompressedFile = fileInRead
    return(uncompressedFile)