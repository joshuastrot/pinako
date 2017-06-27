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

from os import makedirs, listdir, path, walk, remove
from tarfile import open
from shutil import rmtree

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
    packagesListx86 = sshOperations.runCommand(sshClient, "ls /srv/http/%(branch)s/x86_64 | grep '\.xz$'" % locals())[1]
    packagesListi686 = sshOperations.runCommand(sshClient, "ls /srv/http/%(branch)s/i686 | grep '\.xz$'" % locals())[1]

    #Parse Lists
    packagesListx86 = [package.strip() for package in packagesListx86.readlines()]
    packagesListi686 = [package.strip() for package in packagesListi686.readlines()]

    #Generate list of all possible packages:
    packagesList = list(set(packagesListx86) | set(packagesListi686))

    #Populate list with clean package name, and full package file name
    packages = []
    packagesName = []
    packagesDirectory = []
    for package in packagesList:
        packagesDirectory.append(package.strip())
        packagesName.append("-".join(package.strip().split("-")[:-3]))
        packages.append(["-".join(package.strip().split("-")[:-3]), package.strip()])

    #Begin removing any files that were removed upstream
    print("    =[%(branch)s]> Removing packages no longer used." % locals())
    localPackages = listdir("%(target)s/%(branch)s" % locals())

    for package in localPackages:
        if package not in packagesName:
            rmtree("%(target)s/%(branch)s/%(package)s" % locals())

        for root, dirs, files in walk("%(target)s/%(branch)s/%(package)s" % locals()):
            packageArch = root.split("/")[-1]

            if packageArch == "x86_64":
                for file in files:
                    if file and file not in packagesListx86:
                        remove("%(root)s/%(file)s" % locals())
                        if not listdir(root):
                            rmtree(root)
            elif packageArch == "i686":
                for file in files:
                    if file and file not in packagesListi686:
                        remove("%(root)s/%(file)s" % locals())
                        if not listdir(root):
                            rmtree(root)


    #Create new dummy files
    print("    =[%(branch)s]> Create directories of new packages." % locals())
    for package in packagesListx86:
        makedirs("".join((target, "/", branch, "/", "-".join(package.split("-")[:-3]), "/x86_64")), exist_ok=True)
        open("".join((target, "/", branch, "/", "-".join(package.split("-")[:-3]), "/x86_64/", package)), 'a').close()

    for package in packagesListi686:
        makedirs("".join((target, "/", branch, "/", "-".join(package.split("-")[:-3]), "/i686")), exist_ok=True)
        open("".join((target, "/", branch, "/", "-".join(package.split("-")[:-3]), "/i686/", package)), 'a').close()
