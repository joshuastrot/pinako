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

import tarfile

from shutil import move, copytree, rmtree
from os import path, remove, symlink
from subprocess import call
from glob import glob
from datetime import datetime

def prepareCache(target, newPackages, branches = ["winry-stable", "winry-testing"]):
    """
    Prepare the database for uploads by moving new files to the pool, making symlinks, and generating new databases
    """

    print("=> Moving files to pool and symlinking.")

    for package, packageSig in newPackages:
        packageName = package.split("/")[-1]
        packageSigName = packageSig.split("/")[-1]
        if not path.isfile("%(target)s/pool/%(packageName)s" % locals()):
            move(package, "%(target)s/pool/%(packageName)s" % locals())
            symlink("../pool/%(packageName)s" % locals(), package)
        else:
            remove(package)
            symlink("../pool/%(packageName)s" % locals(), package)

        if not path.isfile("%(target)s/pool/%(packageSigName)s" % locals()):
            move(packageSig, "%(target)s/pool/%(packageSigName)s" % locals())
            symlink("../pool/%(packageSigName)s" % locals(), packageSig)
        else:
            remove(packageSig)
            symlink("../pool/%(packageSigName)s" % locals(), packageSig)

def generateDB(target, branches = ["winry-stable", "winry-testing"]):
    """Regenerate the databases with repo-add"""

    print("=> Regenerating package Databases.")

    for branch in branches:
        call(["repo-add", "-q", "-n", "%(target)s/%(branch)s/%(branch)s.db.tar.gz" % locals()] + glob("%(target)s/%(branch)s/*.xz" % locals()))
        if path.exists("%(target)s/%(branch)s/%(branch)s.db.tar.gz.old" % locals()):
            remove("%(target)s/%(branch)s/%(branch)s.db.tar.gz.old" % locals())
        if path.exists("%(target)s/%(branch)s/%(branch)s.files.tar.gz.old" % locals()):
            remove("%(target)s/%(branch)s/%(branch)s.files.tar.gz.old" % locals())

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

def mergeBranches(target, initialBranch, targetBranch):
    """Merge one branch into another branch"""

    print("=> Merging %(initialBranch)s -> %(targetBranch)s" % locals())

    #Copy over the branch
    if path.exists("%(target)s/%(targetBranch)s" % locals()):
        rmtree("%(target)s/%(targetBranch)s" % locals())
    copytree("%(target)s/%(initialBranch)s" % locals(), "%(target)s/%(targetBranch)s" % locals(), symlinks=True)

    #Remove the old databases from the directory
    if path.exists("%(target)s/%(targetBranch)s/%(initialBranch)s.db" % locals()):
        remove("%(target)s/%(targetBranch)s/%(initialBranch)s.db" % locals())
    if path.exists("%(target)s/%(targetBranch)s/%(initialBranch)s.db.tar.gz" % locals()):
        remove("%(target)s/%(targetBranch)s/%(initialBranch)s.db.tar.gz" % locals())
    if path.exists("%(target)s/%(targetBranch)s/%(initialBranch)s.files" % locals()):
        remove("%(target)s/%(targetBranch)s/%(initialBranch)s.files" % locals())
    if path.exists("%(target)s/%(targetBranch)s/%(initialBranch)s.files.tar.gz" % locals()):
        remove("%(target)s/%(targetBranch)s/%(initialBranch)s.files.tar.gz" % locals())
