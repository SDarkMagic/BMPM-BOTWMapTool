import argparse
import oead
import os
from bmpm import functions

def main():
#   Cli Arguments Setup
    progDesc = "A program for bulk replacing and deleting parameters and actors in BotW BYML map files."

    parser = argparse.ArgumentParser(description=progDesc)
    subParser = parser.add_subparsers(description='temp', dest='subParserType')
    parser.add_argument('fileIn', type=str, help="File to open and read data from.")
    parser.add_argument('--noCompression', '-nc', action='store_true', help='Add this if you would prefer the program to not compress the output file with yaz0.')

    editParser = subParser.add_parser('edit', help='edit')
    editParser.add_argument('termToSearch', type=str, help='Term to look through the file and find.')
    editParser.add_argument('--value', '-v', type=str, metavar='value', dest='value', help='Value to match with params found in file.', required=False, default=None)
    editParser.add_argument('replacementTerm', help='Value to replace the original termToSearch value with.')
    editParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1'], help='A value of 0 meaning an integer or 1 meaning a string to set the replacement term as. (defaults to zero)', required=False, default=0)

    remParser = subParser.add_parser('delete', help='delete')
    remParser.add_argument('ActorToDelete', help='The actor name or HashID you would like removed from the map file.')
    remParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1', 'hash', 'name'], help='Type of string that was inputted for actor removal(0 maps to hash and 1 to actor name, will default to actor name.)', required=False, default=1)
    args = parser.parse_args()

#   Global Variables
    fileName = str(args.fileIn).split('.')[0]
    fileExt = ('.' + str(args.fileIn).split('.')[-1])
    fileToOpen = args.fileIn
    openFile = open(fileToOpen, 'rb')


    if (args.subParserType == 'edit'):
        termToSearch = args.termToSearch
        replaceTerm = args.replacementTerm

        replacementParamType = None
        if (int(args.type) == 0):
            replacementParamType = oead.S32(value=int(replaceTerm))
        elif (int(args.type) == 1):
            replacementParamType = str(replaceTerm)

        if (args.value != None):
            valToSearch = args.value
            functions.replaceActor(fileToOpen, fileName, fileExt, termToSearch, valToSearch, replacementParamType, args)
        else:
            functions.replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args)

    elif (args.subParserType == 'delete'):
        actorToDel = args.ActorToDelete
        nameHash = args.type
        functions.removeActor(fileToOpen, fileName, fileExt, actorToDel, nameHash, args)

    else:
        print(f'The option {str(args.subParserType)} could not be found.')

if __name__ == "__main__":
    main()