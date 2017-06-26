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

from os import makedirs
from tarfile import open

from networking import sshOperations

def createCache(target):
    """Create the cache directories"""

    #Begin creating some directories
    makedirs(target, exist_ok=True)
    makedirs("".join((target, "/winry-stable")), exist_ok=True)
    makedirs("".join((target, "/winry-testing")), exist_ok=True)

def updateCache(sshClient, branch, target):
    """Extract an archive and update the cache with new members"""

    #Grab list of packages in the target
    packagesList = sshOperations.runCommand(sshClient, "ls /srv/http/%(branch)s/x86_64 | grep '\.xz$'" % locals())[1]

    packages = []
    for package in packagesList.readlines():
        packages.append(["-".join(package.strip().split("-")[:-3]), package.strip()])

    for package in packages:
        makedirs("".join((target, "/", branch, "/", package[0], "/i686")), exist_ok=True)
        makedirs("".join((target, "/", branch, "/", package[0], "/x86_64")), exist_ok=True)

        open("".join((target, "/", branch, "/", package[0], "/i686/", package[1])), 'a').close()
        open("".join((target, "/", branch, "/", package[0], "/x86_64/", package[1])), 'a').close()
