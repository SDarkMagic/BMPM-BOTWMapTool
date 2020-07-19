import argparse
import oead
import bmpm

# Cli Arguments Setup
progDesc = "A program for bulk replacing parameters withing the '!Parameters' section of BYML map files."
parser = argparse.ArgumentParser(description=progDesc)
parser.add_argument('fileIn', type=str, help="File to open and read data from.")
parser.add_argument('termToSearch', type=str, help='Term to look through the file and find.')
parser.add_argument('replacementTerm', help='Value to replace the original termToSearch value with.')
parser.add_argument('--type', '-t', metavar='value', dest='type', choices=['0', '1'], help='A required value of 0 meaning an integer or 1 meaning a string to set the replacement term as.', required=True)
parser.add_argument('--noCompression', '-nc', action='store_true', help='Add this if you would prefer the program to not compress the output file with yaz0.')
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

if __name__ == '__main__':
    bmpm.replaceParam(fileToOpen, fileName, fileExt, termToSearch, replacementParamType, args)