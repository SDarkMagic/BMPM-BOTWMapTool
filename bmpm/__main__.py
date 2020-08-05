import argparse
import oead
import os
import bmpm as bmpm

def main():
#   Cli Arguments Setup
    progDesc = "A program for bulk replacing and deleting parameters and actors in BotW BYML map files."

    parser = argparse.ArgumentParser(description=progDesc)
    subParser = parser.add_subparsers(description='temp', dest='subParserType')
#    subParser.add_argument('edit', choices=['edit'], help='Edit actor parameters in bulk within a map file.')
    parser.add_argument('fileIn', type=str, help="File to open and read data from.")
    parser.add_argument('--noCompression', '-nc', action='store_true', help='Add this if you would prefer the program to not compress the output file with yaz0.')

    editParser = subParser.add_parser('edit', help='edit')
    editParser.add_argument('termToSearch', type=str, help='Term to look through the file and find.')
    editParser.add_argument('replacementTerm', help='Value to replace the original termToSearch value with.')
    editParser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1'], help='A value of 0 meaning an integer or 1 meaning a string to set the replacement term as. (defaults to zero)', required=False, default=0)
    args = parser.parse_args()

#   Global Variables
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

    if (args.subParserType == 'edit'):
        print('e')
        bmpm.functions.replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args)

if __name__ == "__main__":
    main()