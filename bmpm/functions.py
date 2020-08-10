# functions.py
import oead
import os
import pathlib
import json
from bmpm import util

paramDB = None
dataPath = util.data_dir()

# Function for loading the actor parameter database when necessary
def loadActorDatabase():
    global paramDB
    currentDir = pathlib.Path('./bmpm')
    jsonFile = currentDir / 'paramDB.json'
    if (paramDB == None):
        if (jsonFile.exists() == True):
            open(jsonFile, 'rt')
        else:
            print('The actor parameter database could not be found. Please create one by runnin "bmpm createDB" followed by where the map files from your game dump are stored.')
    return(paramDB)

def checkDataTypes(valIn):
    valOut = None
    try:
        valOut = oead.byml.get_bool(valIn)
    except:
        try:
            valOut = oead.byml.get_double(valIn)
        except:
            try:
                valOut = oead.byml.get_float(valIn)
            except:
                try:
                    valOut = oead.byml.get_int(valIn)
                except:
                    try:
                        valOut = oead.byml.get_int64(valIn)
                    except:
                        try:
                            valOut = oead.byml.get_string(valIn)
                        except:
                            try:
                                valOut = oead.byml.get_uint(valIn)
                            except:
                                try:
                                    valOut = oead.byml.get_uint64(valIn)
                                except:
#                                    print('The specified data did not match any of the BYML data formats. Please double check and see if it is formatted properly.')
                                    valOut = None
    return(valOut)
    

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

# Function for replacing inputted parameter with other user input
def replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args):
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = fileDict.get('Objs')

    for entry in array:
        exactItem = array[iterate]
        entryDict.update(exactItem)
        iterate += 1

        for key in entryDict.keys():
            if (key.lower() == termToSearch.lower()):
                entryDict.update({key: replacementParamType})

        if (entryDict.get('!Parameters') is not None):
#                print('Found "!Parameters" value in entry from file')
            paramDict.update(entryDict.get('!Parameters'))
            for key in paramDict.keys():
#                    print('Checking if param is the same as user input to be replaced')
                if (key.lower() == termToSearch.lower()):
                    paramDict.update({key: replacementParamType})
                    entryDict.update({'!Parameters': paramDict})
#                    print('Successfully replaced parameter')
        
#        print(entryDict)
        objList.append(oead.byml.Hash(entryDict))
        paramDict.clear()
        entryDict.clear()

    fileDict.update({'Objs': objList})
    if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.byml.to_binary(fileDict, False))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, False)))
        print("Compressing file.")
    fileWrite.close()
    print('Done!')

# function for removing all instances of specified actor from a map file
def removeActor(fileToOpen, fileName, fileExt, actorToDel, nameHash, args):
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    deleted = False
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = fileDict.get('Objs')

    if (int(nameHash) == 0 or str(nameHash).lower() == 'hash'):
        actorToDel = int(actorToDel)
        actorToDel = oead.U32(value=actorToDel)
    elif (int(nameHash) == 1 or str(nameHash).lower() == 'name'):
        actorToDel = str(actorToDel)

    for entry in array:
        exactItem = array[iterate]
        entryDict.update(exactItem)
        iterate += 1

        for key in entryDict.keys():
            if (str(entryDict.get(key)).lower() == str(actorToDel).lower()):
                deleted = True

        if (entryDict.get('!Parameters') is not None):
#                print('Found "!Parameters" value in entry from file')
            paramDict.update(entryDict.get('!Parameters'))
            for key in paramDict.keys():
#                    print('Checking if param is the same as user input to be replaced')
                if (str(paramDict.get(key)).lower() == str(actorToDel).lower()):
                    deleted = True
        
#        print(entryDict)
        if (deleted != True):
            objList.append(oead.byml.Hash(entryDict))
        elif (deleted == True):
            paramDict.clear()
            entryDict.clear()
            deleted = False
            continue
        paramDict.clear()
        entryDict.clear()
        deleted = False

    fileDict.update({'Objs': objList})
    if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.byml.to_binary(fileDict, False))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, False)))
        print("Compressing file.")
    fileWrite.close()
    print('Done!')

# more specific version of replaceParam that requires a key: value pair to be searched; e.g. "unitConfigName: Enemy_Guardian_A"
def replaceSpfxParam(fileToOpen, fileName, fileExt, keyToSearch, termToSearch, replacementTerm, args):
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = fileDict.get('Objs')

    for entry in array:
        exactItem = array[iterate]
        entryDict.update(exactItem)
        iterate += 1

        for key in entryDict.keys():
            if (key.lower() == keyToSearch.lower() and str(entryDict.get(key)).lower() == termToSearch.lower()):
                entryDict.update({key: replacementTerm})

        if (entryDict.get('!Parameters') is not None):
#                print('Found "!Parameters" value in entry from file')
            paramDict.update(entryDict.get('!Parameters'))
            for key in paramDict.keys():
#                    print('Checking if param is the same as user input to be replaced')
                if (key.lower() == keyToSearch.lower() and str(entryDict.get(key)).lower() == termToSearch.lower()):
                    paramDict.update({key: replacementTerm})
                    entryDict.update({'!Parameters': paramDict})
#                    print('Successfully replaced parameter')
        
#        print(entryDict)
        objList.append(oead.byml.Hash(entryDict))
        paramDict.clear()
        entryDict.clear()

    fileDict.update({'Objs': objList})
    if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.byml.to_binary(fileDict, False))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, False)))
        print("Compressing file.")

    fileWrite.close()
    print('Done!')

# function for replacing all instances of a specific actor with a new actor including actor specific parameters
def replaceActor(fileToOpen, fileName, fileExt, termToSearch, replacementTerm, args):
    loadActorDatabase()
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = fileDict.get('Objs')

    for entry in array:
        exactItem = array[iterate]
        entryDict.update(exactItem)
        iterate += 1

        for key in entryDict.keys():
            if (key.lower() == keyToSearch.lower() and str(entryDict.get(key)).lower() == termToSearch.lower()):
                entryDict.update({key: replacementTerm})

        if (entryDict.get('!Parameters') is not None):
#                print('Found "!Parameters" value in entry from file')
            paramDict.update(entryDict.get('!Parameters'))
            for key in paramDict.keys():
#                    print('Checking if param is the same as user input to be replaced')
                if (key.lower() == keyToSearch.lower() and str(entryDict.get(key)).lower() == termToSearch.lower()):
                    paramDict.update({key: replacementTerm})
                    entryDict.update({'!Parameters': paramDict})
#                    print('Successfully replaced parameter')
        
#        print(entryDict)
        objList.append(oead.byml.Hash(entryDict))
        paramDict.clear()
        entryDict.clear()

    fileDict.update({'Objs': objList})
    if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.byml.to_binary(fileDict, False))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, False)))
        print("Compressing file.")

    fileWrite.close()
    print('Done!')

# a function for generating the necessary actor database from ones game dump
def genActorDatabase(mapDir):
    mapDir = pathlib.Path(mapDir)
    fileList = util.checkDir(mapDir)
    DBPath = pathlib.Path(dataPath / 'actorParamDatabase.json')
    if DBPath.exists():
        actorDatabaseFileRead = open(DBPath, 'rt')
        paramDict = json.loads(actorDatabaseFileRead.read())
        actorDatabaseFileRead.close()
    else:
        paramDict = {}
    fileDict = {}
    iterCount = 0
    
    for filePath in fileList:
        fileOpen = open(filePath, 'rb')
        uncompressedFile = checkCompression(fileOpen.read())
        extractByml = oead.byml.from_binary(uncompressedFile)
        for key in extractByml.keys():
            fileDict.update({key: extractByml.get(key)})
        array = fileDict.get('Objs')
        for subDict in array:
            entryDict = {}
            exactItem = array[iterCount]
            entryDict.update(exactItem)
            subParamDict = {}
            iterCount += 1
            objName = entryDict.get('UnitConfigName')
            if objName in paramDict.keys():
                continue
            else:
                if entryDict.get('!Parameters') != None:
                    subParamDict.update(dict(entryDict.get('!Parameters')))
                    for key in subParamDict.keys():
                        testVal = subParamDict.get(key)
                        valOut = checkDataTypes(testVal)
                        if valOut != None:
                            subParamDict.update({key: valOut})
                        else:
                            print('Sub-dict entry was set to None')
                            subParamDict.update({key: valOut})
                            continue
                else:
                    subParamDict = None
                paramDict.update({objName: subParamDict})
        fileOpen.close()
        iterCount = 0
    actorDatabaseFileWrite = open(DBPath, 'wt')
    actorDatabaseFileWrite.write(json.dumps(paramDict, indent=2))
    actorDatabaseFileWrite.close()
    print(f'File was saved to {DBPath}')
