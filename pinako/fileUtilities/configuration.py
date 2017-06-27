#!/usr/bin/env python

#   This file is part of Pinako - <http://github.com/joshuastrot/pinako>
#
#   Copyright 2017, Joshua Strot <joshuastrot@gmail.com>
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

from os import path, environ, makedirs
from shutil import copyfile
from yaml import load, dump
from getpass import getuser

from networking import verification

def findXDGConfig():
    """Find the XDG config directory"""

    #Grab the XDG Path
    if environ.get("XDG_CONFIG_HOME"):
        xdgConfig = environ["XDG_CONFIG_HOME"]
    else:
        xdgConfig = path.expanduser("~") + "/.config"
    return xdgConfig

def configure():
    """Configure the configuration file"""

    print("=> Now configuring for your user.")

    #Ask about the location of SSH key
    print("    => What is the absolute path to your SSH key?")
    sshKey = input("".join(("    =[", path.expanduser("~"), "/.ssh/id_rsa]> ")))

    #Check if defaulted and is absolute path
    sshKey = "".join((path.expanduser("~"), "/.ssh/id_rsa")) if not sshKey else sshKey

    if not path.isabs(sshKey):
        print("=> Error! SSH Key path is not absolute. Please use an absolute path.")
        exit(1)

    #Ask about user name
    print("    => What is the SSH username for your Pinako account")
    username = input("".join(("    =[", getuser(), "]> ")))

    #Check if defaulted
    username = getuser() if not username else username

    #Ask about Winry server address
    print("    => What is the IP address of the Winry server?")
    serverAddress = input("".join(("    => ")))

    if not serverAddress or not verification.verifyAddress(serverAddress):
        print("=> Error! Invalid IP address of the Winry Server")
        exit(1)

    return {
        "ServerAddress": serverAddress,
        "Username": username,
        "SSHKey": sshKey
    }



def loadConfiguration():
    """Load the YAML configuration file for pinako"""

    #Find XDG Configuration directory and set some variables
    xdgConfig = findXDGConfig()

    pinakoConfig = "".join((xdgConfig, "/pinako/pinako.yaml"))
    pinakoDirectory = "".join((xdgConfig, "/pinako"))

    #Make the pinako directory if not already created
    if not path.isdir(pinakoDirectory):
        makedirs(pinakoDirectory)

    #Create a pinako config if not already present
    customConfiguration = {}
    if not path.isfile(pinakoConfig):
        print("=> No user defined configuration file yet, creating one.")
        copyfile("/usr/share/pinako/data/pinako.yaml", pinakoConfig)
        customConfiguration = configure()

    #Load the pinako config file
    try:
        with open(pinakoConfig, "r") as file:
            configurationContents = load(file)
            if (not configurationContents["Username"] or not configurationContents["SSHKey"]\
                or not configurationContents["ServerAddress"]) and not customConfiguration:

                customConfiguration = configure()
    except IOError as e:
        print("=> Error! Could not load new configuration file.")
        print(e)
        exit(1)

    return {**configurationContents, **customConfiguration}

def writeConfiguration(cachePath, configuration):
    """Write a YAML configuration to the user specified configuration file"""

    #Load the XDG Configuration path
    xdgConfig = findXDGConfig()

    pinakoConfig = "".join((xdgConfig, "/pinako/pinako.yaml"))

    #Make sure the configuration exists and something funky didn't happen
    if not path.isfile(pinakoConfig):
        print("=> Error! The configuration file was deleted.")
        exit(1)

    #Write to the configuration file
    try:
        with open(pinakoConfig, "w") as file:
            configuration["Cache"] = cachePath
            dump(configuration, file)
    except IOError as e:
        print("=> Error! Could not write to new configuration file.")
        print(e)
