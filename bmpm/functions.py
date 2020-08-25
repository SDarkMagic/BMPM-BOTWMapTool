# functions.py
import oead
import os
import pathlib
import json
import blwp
from bmpm import util

dataPath = util.data_dir()



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
    

# Function for replacing inputted parameter with other user input
def replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args):
    endian = args.endian
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = util.checkCompression(fileToOpen)
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
            fileWrite.write(oead.byml.to_binary(fileDict, big_endian=bool(endian)))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, big_endian=bool(endian))))
        print("Compressing file.")
    fileWrite.close()
    print('Done!')

# function for removing all instances of specified actor from a map file
def removeActor(fileToOpen, fileName, fileExt, actorToDel, nameHash, args):
    keysToRem = []
    endian = args.endian
    fileDict = {}
    entryDict = {}
    iterate = 0
    objList = []
    deleted = False
    if (args.subStr == True):
        startWith = True
    else:
        startWith = False
#    print(fileExt)
    if fileExt == '.sblwp' or fileExt == '.blwp':
        fileToOpen = pathlib.Path(fileToOpen)
        decodedData = blwp.prod.decoder(fileToOpen)
        for key in decodedData.keys():
            if startWith == True:
                if str(key).lower().startswith(str(actorToDel).lower()) == True:
                    keysToRem.append(key)
                else:
                    continue
            elif startWith == False:
                if str(key).lower() == str(actorToDel).lower():
                    keysToRem.append(key)
                else:
                    continue
            else:
                print('error')
                continue
        for key in keysToRem:
            decodedData.pop(key)
        if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(blwp.prod.encoder(decodedData))
            return

        else:
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.yaz0.compress(blwp.prod.encoder(decodedData)))
            print("Compressing file.")
        fileWrite.close()
        print('Done!')
        return
    elif fileExt == '.smubin' or fileExt == '.mubin':
        fileToOpen = open(fileToOpen, 'rb').read()
        uncompressedFile = util.checkCompression(fileToOpen)
        extractByml = oead.byml.from_binary(uncompressedFile)
        for key in extractByml.keys():
            fileDict.update({key: extractByml.get(key)})
        array = fileDict.get('Objs')

        if (int(nameHash) == 0 or str(nameHash).lower() == 'hash'):
            actorToDel = int(actorToDel)
            actorToDel = oead.U32(value=actorToDel)
        elif (int(nameHash) == 1 or str(nameHash).lower() == 'name'):
            actorToDel = str(actorToDel)
        if (array != None):
            for entry in array:
                exactItem = array[iterate]
                entryDict.update(exactItem)
                iterate += 1

                for key in entryDict.keys():
                    if (startWith == True):
                        if (str(entryDict.get(key)).lower().startswith(str(actorToDel).lower()) == True):
                                deleted = True
                    elif(startWith == False):
                        if (str(entryDict.get(key)).lower() == str(actorToDel).lower()):
                            deleted = True
                    else:
                        deleted = False

                if (deleted != True):
                    objList.append(oead.byml.Hash(entryDict))
                elif (deleted == True):
                    entryDict.clear()
                    deleted = False
                    continue
                entryDict.clear()
                deleted = False

            fileDict.update({'Objs': objList})
            if (args.noCompression):
                extList = []
                fileExt = fileExt.lstrip('.s')
                fileExt = ('.') + fileExt
                fileWrite = open(fileName + fileExt, 'wb')
                fileWrite.write(oead.byml.to_binary(fileDict, big_endian=bool(endian)))
                return

            else:
                fileWrite = open(fileName + fileExt, 'wb')
                fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, big_endian=bool(endian))))
                print("Compressing file.")
            fileWrite.close()
            print('Done!')
            return
        else:
            print('could not find "Objs" parameter in the map file.')
            return

# more specific version of replaceParam that requires a key: value pair to be searched; e.g. "unitConfigName: Enemy_Guardian_A"
def replaceSpfxParam(fileToOpen, fileName, fileExt, keyToSearch, termToSearch, replacementTerm, args):
    endian = args.endian
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = util.checkCompression(fileToOpen)
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
            fileWrite.write(oead.byml.to_binary(fileDict, big_endian=bool(endian)))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, big_endian=bool(endian))))
        print("Compressing file.")

    fileWrite.close()
    print('Done!')

# function for replacing all instances of a specific actor with a new actor including actor specific parameters
def replaceActor(fileToOpen, fileName, fileExt, nameHash, convFrom, convTo, args):
    endian = args.endian
    try:
        paramDB = util.loadActorDatabase()
    except:
        return
    if (args.subStr == True):
        startWith = True
    else:
        startWith = False
    fileDict = {}
    paramDict = {}
    entryDict = {}
    iterate = 0
    objList = []
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = util.checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = list(fileDict.get('Objs'))

    if (int(nameHash) == 0 or str(nameHash).lower() == 'hash'):
        convFrom = oead.U32(value=int(convFrom))
    elif (int(nameHash) == 1 or str(nameHash).lower() == 'name'):
        convFrom = str(convFrom)

    if (convTo in paramDB.keys()):
        for entry in array:
            exactItem = dict(entry)
#            print(dict(entry))
            entryDict.update(exactItem)
            iterate += 1

            for key in entryDict.keys():
                if (startWith == True):
                    if (str(entryDict.get(key)).lower().startswith(str(convFrom).lower()) == True):
                        entryDict.update({'UnitConfigName': convTo})
#                        print('using startswith')
#                        print(dict(entryDict.get('!Parameters')))
                        if (paramDB.get(convTo) is not None):
                            paramDBGet = util.dictParamsToByml(paramDB.get(convTo))
                            paramDict.update((paramDBGet))
#                            print(paramDict)
#                           print(paramDBGet)
                            entryDict.update({"!Parameters": dict(paramDict)})
#                            print(oead.byml.Hash(paramDict))
#                            print(entryDict)
#                            print(paramDict)
#                            entryDict.update({"!Parameters": paramDict})
#                            print(util.dictParamsToByml(paramDB.get(convTo)))
                        else:
                            try:
                                entryDict.pop(str("!Parameters"))
                            except:
                                continue
                        break
                    else:
                        continue

                elif(startWith == False):
                    if (str(entryDict.get(key)).lower() == str(convFrom).lower()):
                        entryDict.update({'UnitConfigName': convTo})
#                        print(dict(entryDict.get('!Parameters')))
                        if (paramDB.get(convTo) is not None):
                            paramDBGet = util.dictParamsToByml(paramDB.get(convTo))
                            paramDict.update((paramDBGet))
#                            print(paramDict)
#                           print(paramDBGet)
                            entryDict.update({"!Parameters": dict(paramDict)})
#                            print(oead.byml.Hash(paramDict))
#                            print(entryDict)
#                            print(paramDict)
#                            entryDict.update({"!Parameters": paramDict})
#                            print(util.dictParamsToByml(paramDB.get(convTo)))
                        else:
                            try:
                                entryDict.pop(str("!Parameters"))
                            except:
                                continue
                        break
                    else:
                        continue
                else:
                    print('How did you end up here?')
                    return
#            try:
#                print(dict(dict(entryDict).get('!Parameters')))
#            except:
#                print('woops')
            objList.append(dict(entryDict))
            entryDict.clear()
            paramDict.clear()
#        print(objList)
#        print(objList)
        fileDict.update({'Objs': oead.byml.Array(objList)})
        fileDict = (fileDict)
        if (args.noCompression):
                extList = []
                fileExt = fileExt.lstrip('.s')
                fileExt = ('.') + fileExt
                fileWrite = open(fileName + fileExt, 'wb')
                fileWrite.write(oead.byml.to_binary(fileDict, big_endian=bool(endian)))

        else:
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, big_endian=bool(endian))))
            print("Compressing file.")

        fileWrite.close()
        print('Done!')
    else:
        print(f'Error: Could not find the value {convTo} in the database. Check your spelling and/or capitalization or try regenerating the database.')

# a function for generating the necessary actor database from ones game dump
def genActorDatabase(mapDir):
    mapDir = pathlib.Path(mapDir)
    mapFileList = util.checkDir(mapDir)
    DBPath = pathlib.Path(dataPath / 'actorParamDatabase.json')
    if DBPath.exists():
        actorDatabaseFileRead = open(DBPath, 'rt')
        paramDict = json.loads(actorDatabaseFileRead.read())
        actorDatabaseFileRead.close()
    else:
        paramDict = {}
    fileDict = {}
#    iterCount = 0
    
    for filePath in mapFileList:
#        print(mapFileList)
#        print(filePath)
        fileOpen = open(filePath, 'rb')
        uncompressedFile = util.checkCompression(fileOpen.read())
        extractByml = oead.byml.from_binary(uncompressedFile)
        for key in extractByml.keys():
            fileDict.update({key: extractByml.get(key)})
        try:
            array = list(fileDict.get('Objs'))
        except:
            continue
        if array != None:
            for dictObj in array:
                entryDict = {}
                exactItem = dict(dictObj)
                entryDict.update(dict(exactItem))
                subParamDict = {}
#                iterCount += 1
                objName = entryDict.get('UnitConfigName')
                if objName in paramDict.keys():
                    entryDict.clear()
                    continue
                else:
                    if entryDict.get("!Parameters") != None:
                        subParamDict.update(dict(entryDict.get('!Parameters')))
                        for key in subParamDict.keys():
                            testVal = subParamDict.get(key)
                            valOut = checkDataTypes(testVal)
#                            print(valOut)
                            subParamDict.update({key: valOut})
                    else:
                        continue
                    paramDict.update({objName: dict(subParamDict)})
                subParamDict.clear()
            fileOpen.close()
#                iterCount = 0
        else:
            print('No map files could be found...')        

    actorDatabaseFileWrite = open(DBPath, 'wt')
    actorDatabaseFileWrite.write(json.dumps(paramDict, indent=2))
    actorDatabaseFileWrite.close()
    print(f'File was succesfully saved to {DBPath}')

# Small function for changing the endianness of the map file
def swapEnd(fileToOpen, fileName, fileExt, args):
    fileToOpen = open(fileToOpen, 'rb').read()
    uncompressedFile = util.checkCompression(fileToOpen)
    extractByml = oead.byml.from_binary(uncompressedFile)
    
    if uncompressedFile[:2] == b"BY":
        endian = False
    elif uncompressedFile[:2] == b"YB":
        endian = True
    else:
        print('The endianness of the file could not be identified, most likely due to an invalid magic.')
        return

    fileDict = dict(extractByml)
    if endian == True:
        print('Converting file to big endian.')
    else:
        print('Converting file to little endian.')
    if (args.noCompression):
            extList = []
            fileExt = fileExt.lstrip('.s')
            fileExt = ('.') + fileExt
            fileWrite = open(fileName + fileExt, 'wb')
            fileWrite.write(oead.byml.to_binary(fileDict, big_endian=bool(endian)))

    else:
        fileWrite = open(fileName + fileExt, 'wb')
        fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, big_endian=bool(endian))))
        print("Compressing file.")

    fileWrite.close()
    print('Done!')