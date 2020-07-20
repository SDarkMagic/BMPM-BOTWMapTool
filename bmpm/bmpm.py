import oead
import os
import argparse


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