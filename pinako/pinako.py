#!/usr/bin/env python

#   This file is part of Pinako - <http://github.com/winry-linux/pinako>
#
#   Copyright 2017, Joshua Strot <joshua@winrylinux.org>
#
#   Pinako is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Pinako is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Pinako. If not, see <http://www.gnu.org/licenses/>.

import argparse

from sys import argv
from os import geteuid, symlink

from display import *
from configure import *
from ssh import *
from cache import *

#Exit if root
if geteuid() == 0:
    print("This program cannot be ran as root")
    exit(0)

#Set up the argument parser, add the needed options
parser = argparse.ArgumentParser(description='Control the central repository of Winry Linux.')
parserGroup = parser.add_mutually_exclusive_group()
parserGroup.add_argument('-i', "--init", type=str, metavar="PATH", help="Initialize the cache at the given absolute path")
parserGroup.add_argument('-d', "--download", action="store_true", help="Download changes from repository")
parserGroup.add_argument('-s', "--show", action="store_true", help="Show the currently staged changes")
parserGroup.add_argument('-v', "--verify", action="store_true", help="Verify the repository is safe to upload")
parserGroup.add_argument('-u', "--upload", action="store_true", help="Upload current repository changes")
parserGroup.add_argument('-m', "--merge", type=str, nargs=2, metavar=("SOURCE", "TARGET"), help="Merge one branch into another")
parserGroup.add_argument('-c', "--compare", type=str, nargs=2, metavar=("SOURCE", "TARGET"), help="Compare one branch to another")
parserGroup.add_argument('-f', "--unlock", action="store_true", help="Force unlock the server")
parserGroup.add_argument('-l', "--lock", action="store_true", help="Force lock the server")

#Output help if no argument is passed, exit
if len(argv) == 1:
    asciiArt.banner()
    parser.print_help()
    exit(1)

#Display the banner
asciiArt.banner()

#Parse args
args=parser.parse_args()

#Load the configuration file
configurationData = configurationFile.loadConfiguration()

#Set the targetDirectory
targetDirectory = configurationData["Cache"]

#Begin running the main program
if args.init:
    #Override targetDirectory
    targetDirectory = args.init

    #Instantiate the SSHClient object
    sshClient = sshClient.sshClient(configurationData["Username"], configurationData["ServerAddress"], configurationData["SSHKey"])

    #Load all the files for the cache
    initialize.loadFiles(sshClient, targetDirectory, configurationData["ServerSSHPath"], configurationData["Branches"])

    #Write the new cache location
    configurationFile.writeConfiguration(targetDirectory, configurationData)

elif args.download:
    #Instantiate the SSHClient object
    sshClient = sshClient.sshClient(configurationData["Username"], configurationData["ServerAddress"], configurationData["SSHKey"])

    #Load all the files for the Cache
    initialize.loadFiles(sshClient, targetDirectory, configurationData["ServerSSHPath"], configurationData["Branches"])

elif args.show:
    #Search the cache for new files
    search.regular(targetDirectory, configurationData["Branches"])

elif args.verify:
    #Verify the repository
    safe = search.verifyRepository(targetDirectory, configurationData["Branches"])

elif args.upload:
    #Make sure the cache is safe
    safe = search.verifyRepository(targetDirectory, configurationData["Branches"])

    #Find list of new packages
    newFiles = search.regular(targetDirectory, configurationData["Branches"])

    if not newFiles:
        print("=> Nothing to do!")
        #exit(1)

    #Move new files to pool and make new symlinks
    prepare.prepareCache(targetDirectory, newFiles, configurationData["Branches"])

    #Regenerate the DB's
    prepare.generateDB(targetDirectory, configurationData["Branches"])

    #Update the state file
    prepare.modifyState(targetDirectory, configurationData["PackagerName"], configurationData["PackagerEmail"])

    #Compress to tar
    prepare.compress(targetDirectory)

    #Instantiate the SSHClient object
    sshClient = sshClient.sshClient(configurationData["Username"], configurationData["ServerAddress"], configurationData["SSHKey"])

    #Update the server
    updateServer.updateServer(sshClient, configurationData["PackagerName"], configurationData["PackagerEmail"], configurationData["ServerSSHPath"], configurationData["Branches"])

elif args.compare:
    #Compare the branches
    search.compareBranches(targetDirectory, args.compare, configurationData["Branches"])

elif args.merge:
    #Make sure the cache is safe
    safe = search.verifyRepository(targetDirectory, configurationData["Branches"])

    #Show the changes to be made
    search.compareBranches(targetDirectory, args.merge, configurationData["Branches"])

    #Merge the branches
    prepare.mergeBranches(targetDirectory, args.merge[0], args.merge[1])

elif args.unlock:
    #Instantiate the SSHClient object
    sshClient = sshClient.sshClient(configurationData["Username"], configurationData["ServerAddress"], configurationData["SSHKey"])

    #Verify user is sure
    print("=> Are you absolutely sure you would like to unlock the server? Someone may be uploading.")
    verification = input("=[y/N]> ")

    if verification != "y" and verification != "Y":
        print("=> Exiting.")
        exit(1)

    #Unlock server
    sshClient.unlockServer(configurationData["ServerSSHPath"])

elif args.lock:
    #Instantiate the SSHClient object
    sshClient = sshClient.sshClient(configurationData["Username"], configurationData["ServerAddress"], configurationData["SSHKey"])

    #Verify user is sure
    print("=> Are you absolutely sure you would like to lock the server? You will need to manually unlock it.")
    verification = input("=[y/N]> ")

    if verification != "y" and verification != "Y":
        print("=> Exiting.")
        exit(1)

    #lock server
    sshClient.lockServer(configurationData["PackagerName"], configurationData["PackagerEmail"], configurationData["ServerSSHPath"])
