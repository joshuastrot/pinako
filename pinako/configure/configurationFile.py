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

from os import path, environ
from yaml import load, dump

def findXDGConfig():
    """Find the XDG config directory"""

    #Grab the XDG Path
    if environ.get("XDG_CONFIG_HOME"):
        xdgConfig = environ["XDG_CONFIG_HOME"]
    else:
        xdgConfig = path.expanduser("~") + "/.config"
    return xdgConfig


def loadConfiguration():
    """Load the YAML configuration file for pinako"""

    #Find XDG Configuration directory and set some variables
    xdgConfig = findXDGConfig()

    pinakoConfig = "".join((xdgConfig, "/pinako/pinako.yaml"))
    pinakoDirectory = "".join((xdgConfig, "/pinako"))

    #Error out if no configuration file.
    customConfiguration = {}
    if not path.isfile(pinakoConfig):
        print("=> No user defined configuration file. Please create one.")
        exit(1)

    #Load the pinako config file
    try:
        with open(pinakoConfig, "r") as file:
            configurationContents = load(file)
    except IOError as e:
        print("=> Error! Could not load configuration file.")
        print(e)
        exit(1)

    return configurationContents

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
