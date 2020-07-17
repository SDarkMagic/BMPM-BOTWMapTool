import oead
import os
import sys
import argparse


# Cli Arguments Setup
progDesc = "A program for bulk replacing parameters withing the '!Parameters' section of BYML map files."
parser = argparse.ArgumentParser(description=progDesc)
parser.add_argument('fileIn', type=str, help="File to open and read data from.")
parser.add_argument('termToSearch', type=str, help='Term to look through the file and find.')
parser.add_argument('replacementTerm', help='Value to replace the original termToSearch value with.')
parser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1'], help='A required value of 0 meaning an integer or 1 meaning a string to set the replacement term as.', required=True)
args = parser.parse_args()


# Global Variables
fileName = str(args.fileIn).split('.')[0]
fileExt = ('.' + str(args.fileIn).split('.')[-1])
fileToOpen = args.fileIn
openFile = open(fileToOpen, 'rb')
termToSearch = args.termToSearch
replaceTerm = args.replacementTerm

replacementParamType = None
if (int(args.type) == 0):
    replacementParamType = oead.S32(value=int(replaceTerm))
elif (int(args.type) == 1):
    replacementParamType = str(replaceTerm)


# A function for checking if a file is yaz0 compressed and then determining whether or not to decompress it based off of that
def checkCompression(fileCheck):
    fileInRead = fileCheck.read()
    if (oead.yaz0.get_header(fileInRead) is not None):
        print("File is Yaz0 compressed, decompressing")
        uncompressedFile = oead.yaz0.decompress(fileInRead)
    else:
        print('File is not compressed with Yaz0')
        uncompressedFile = fileCheck
    return(uncompressedFile)

# Function for replacing inputted parameter with other user input
def replaceParam(fileToOpen):
    fileDict = {}
    entryDict = {}
    paramDict = {}
    iterate = 0
    objList = []
    uncompressedFile = checkCompression(openFile)
    extractByml = oead.byml.from_binary(uncompressedFile)
    for key in extractByml.keys():
        fileDict.update({key: extractByml.get(key)})
    array = fileDict.get('Objs')
    fileWrite = open(fileName + fileExt, 'wb')

    for entry in array:
        exactItem = array[iterate]
        entryDict.update(exactItem)
        iterate += 1
        if (entryDict.get('!Parameters') is not None):
            print('Found "!Parameters" value in entry from file')
            paramDict.update(entryDict.get('!Parameters'))
            for key in paramDict.keys():
                print('Checking if param is the same as user input to be replaced')
                if (key == termToSearch):
                    paramDict.update({termToSearch: replacementParamType})
                    entryDict.update({'!Parameters': paramDict})
                    print('Successfully replaced parameter')
        
        print(entryDict)
        objList.append(oead.byml.Hash(entryDict))
        paramDict.clear()
        entryDict.clear()

    fileDict.update({'Objs': objList})
#    print(objList)
    fileWrite.write(oead.yaz0.compress(oead.byml.to_binary(fileDict, False)))
#    oead.yaz0.compress(fileWrite.read())
    fileWrite.close()


if __name__ == '__main__':
#    outFile.write('Objs:\n')
#    outFile.close()
    replaceParam(openFile)
    openFile.close()
    print("done")
