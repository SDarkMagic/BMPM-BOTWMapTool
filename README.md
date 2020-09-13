# BMPM (Botw Map Parameter Manipulator)
 A script for manipulating parameters contained within BotW's map files in bulk.

# Installation
 Copy the ".exe" file to C:/Users/(username)/AppData/local/Programs/Python/scripts/ OR add the directory containing the compiled script to your PATH (Please note that the exe is not up to date)
 <br>
 OR
 <br>
 Use the command "pip install bmpm" from the cli to automatically install the and setup necessarry files
 <br>
 OR
 <br>
 Download a zip of the code and run "python setup.py install" from the cli within the directory containing the files to install and setup the files

# Usage
 The batch (currently outdated) file included is for recursively going through directories and editing all "LevelSensorMode" parameters to 1
 To delete an actor or set of actors, use `bmpm delete`; for editing paramaters, use `bmpm edit`.
 For more information on how to use the script, type "bmpm -h" or "bmpm --help"

# To-Do
 Create UI
 <br>
 ~~Implement recursive file handling~~
 <br>
 Option to delete all actors linked to one being deleted.
 <br>
 ~~Add option for big endian so that the wiiU/Cemu plebs can also use the tool~~
 <br>
 Incorporate into Ice Spear's UI?
 <br>
 Add function to add entries to the "!Parameters" section of an actor in a map file.