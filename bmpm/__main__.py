# __main__.py
import argparse
import oead
import os
import pathlib
from bmpm import functions
from bmpm import util

def main():
#   Cli Arguments Setup
    progDesc = "A program for bulk replacing and deleting parameters and actors in BotW BYML map files."

    parser = argparse.ArgumentParser(description=progDesc)
    subParser = parser.add_subparsers(description='Sub-Commands required to use the functions of BMPM', dest='subParserType')
    parser.add_argument('fileIn', type=str, help="File to open and read data from.")
    parser.add_argument('--noCompression', '-nc', action='store_true', help='Add this if you would prefer the program to not compress the output file with yaz0.')
    parser.add_argument('--bigEndian', '-be', action='store_true', dest='endian', help='Outputs the files in a big endian format', required=False, default=False)

    editParser = subParser.add_parser('edit', help='edit')
    editParser.add_argument('termToSearch', type=str, help='Term to look through the file and find.')
    editParser.add_argument('--value', '-v', type=str, metavar='value', dest='value', help='Value to match with params found in file.', required=False, default=None)
    editParser.add_argument('replacementTerm', help='Value to replace the original termToSearch value with.')
    editParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1'], help='A value of 0 meaning an integer or 1 meaning a string to set the replacement term as. (defaults to zero)', required=False, default=0)

    remParser = subParser.add_parser('delete', help='Remove an actor or actors from the map file(s) based on either name or hashID')
    remParser.add_argument('ActorToDelete', help='The actor name or HashID you would like removed from the map file.')
    remParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1', 'hash', 'name'], help='Type of string that was inputted for actor removal(0 maps to hash and 1 to actor name, will default to actor name.)', required=False, default=1)

    convParser = subParser.add_parser('convert', help='Converts one actor to another based off of a template.')
    convParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1', 'hash', 'name'], help='Type of string that was inputted for actor removal(0 maps to hash and 1 to actor name, will default to actor name.)', required=False, default=1)
    convParser.add_argument('actorConvertFrom', help='The actor name or hashID you would like to be converted.')
    convParser.add_argument('actorConvertTo', type=str, help='Actor to convert to.')

    genParser = subParser.add_parser('genDB', help='Generate the database of actors necessary for using the replace actor function. Only needs to be run once.')


#   Global Variables
    args = parser.parse_args()
    fileToOpen = pathlib.Path(args.fileIn)
    fileToOpen = fileToOpen
    if fileToOpen.is_file():
        fileObj = fileToOpen
        fileName = str(fileObj).split('.')[0]
        fileExt = ('.' + str(fileObj).split('.')[-1])
    else:
        print('Directory entered, beginning recursive processes.')


    if (args.subParserType == 'edit'):
        termToSearch = args.termToSearch
        replaceTerm = args.replacementTerm
        replacementParamType = None
        if (int(args.type) == 0):
            replacementParamType = oead.S32(value=int(replaceTerm))
        elif (int(args.type) == 1):
            replacementParamType = str(replaceTerm)



        if fileToOpen.is_dir():
            fileList = util.checkDir(fileToOpen)
            for fileToOpen in fileList:
                fileName = str(fileToOpen).split('.')[0]
                fileExt = ('.' + str(fileToOpen).split('.')[-1])

                if (args.value != None):
                    valToSearch = args.value
                    functions.replaceSpfxParam(fileToOpen, fileName, fileExt, termToSearch, valToSearch, replacementParamType, args)
                else:
                    functions.replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args)
        else:
            if (args.value != None):
                valToSearch = args.value
                functions.replaceSpfxParam(fileToOpen, fileName, fileExt, termToSearch, valToSearch, replacementParamType, args)
            else:
                functions.replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args)

    elif (args.subParserType == 'delete'):
        actorToDel = args.ActorToDelete
        nameHash = args.type
        if fileToOpen.is_dir():
            fileList = util.checkDir(fileToOpen)
            for fileToOpen in fileList:
                fileName = str(fileToOpen).split('.')[0]
                fileExt = ('.' + str(fileToOpen).split('.')[-1])
                functions.removeActor(fileToOpen, fileName, fileExt, actorToDel, nameHash, args)
        else:
            functions.removeActor(fileToOpen, fileName, fileExt, actorToDel, nameHash, args)

    elif (args.subParserType == 'convert'):
        actorToConv = args.actorConvertFrom
        actorConvTo = args.actorConvertTo
        nameHash = args.type 
        if fileToOpen.is_dir():
            fileList = util.checkDir(fileToOpen)
            for fileToOpen in fileList:
                fileName = str(fileToOpen).split('.')[0]
                fileExt = ('.' + str(fileToOpen).split('.')[-1])
                functions.replaceActor(fileToOpen, fileName, fileExt, nameHash, actorToConv, actorConvTo, args)
        else:
            functions.replaceActor(fileToOpen, fileName, fileExt, nameHash, actorToConv, actorConvTo, args)

    elif(args.subParserType == 'genDB'):
        if (input('This may take a while, are you sure you would like to continue? (y/n)').lower().startswith('y')):
            functions.genActorDatabase(fileToOpen)
        else:
            print('Cancelling operation.')

    else:
        print(f'The option {str(args.subParserType)} could not be found.')

if __name__ == "__main__":
    main()