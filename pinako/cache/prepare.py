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

import tarfile

from shutil import move
from os import path, remove, symlink
from subprocess import call
from glob import glob
from datetime import datetime

def prepareCache(target, newPackages, branches = ["winry-stable", "winry-testing"], architectures = ["i686", "x86_64"]):
    """
    Prepare the database for uploads by moving new files to the pool, making symlinks, and generating new databases
    """

    print("=> Moving files to pool and symlinking.")

    for package, packageSig in newPackages:
        packageName = package.split("/")[-1]
        packageSigName = packageSig.split("/")[-1]
        if not path.isfile("%(target)s/pool/%(packageName)s" % locals()):
            move(package, "%(target)s/pool/%(packageName)s" % locals())
            symlink("../../pool/%(packageName)s" % locals(), package)
        else:
            remove(package)
            symlink("../../pool/%(packageName)s" % locals(), package)

        if not path.isfile("%(target)s/pool/%(packageSigName)s" % locals()):
            move(packageSig, "%(target)s/pool/%(packageSigName)s" % locals())
            symlink("../../pool/%(packageSigName)s" % locals(), packageSig)
        else:
            remove(packageSig)
            symlink("../../pool/%(packageSigName)s" % locals(), packageSig)

def generateDB(target, branches = ["winry-stable", "winry-testing"], architectures = ["i686", "x86_64"]):
    """Regenerate the databases with repo-add"""

    print("=> Regenerating package Databases.")

    for branch in branches:
        for arch in architectures:
            call(["repo-add", "-q", "-n", "%(target)s/%(branch)s/%(arch)s/%(branch)s.db.tar.gz" % locals()] + glob("%(target)s/%(branch)s/%(arch)s/*.xz" % locals()))
            if path.exists("%(target)s/%(branch)s/%(arch)s/%(branch)s.db.tar.gz.old" % locals()):
                remove("%(target)s/%(branch)s/%(arch)s/%(branch)s.db.tar.gz.old" % locals())
            if path.exists("%(target)s/%(branch)s/%(arch)s/%(branch)s.files.tar.gz.old" % locals()):
                remove("%(target)s/%(branch)s/%(arch)s/%(branch)s.files.tar.gz.old" % locals())

def compress(target):
    """Compress the repository into a tar file for upload"""

    print("=> Compressing repository.")

    archive = tarfile.open("/tmp/pinako-upload.tar", "w")
    archive.add(target, arcname=".")
    archive.close()

def modifyState(target, packagerName, packagerEmail):
    """Update the state file"""

    print("=> Updating state file")

    try:
        with open("%(target)s/state" % locals(), "w") as state:
            time = datetime.now().time()
            state.write("Packager: %(packagerName)s\nPackagerEmail: %(packagerEmail)s\nUpdated: %(time)s" %locals())
    except IOError as e:
        print("=> Error! Could not write to state.")
        exit(1)
