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

from os import path, walk, listdir

def regular(target, branches = ["winry-stable", "winry-testing"], architectures = ["i686", "x86_64"]):
    """Check the cache for regular, non database files"""

    newPackages = []
    for branch in branches:
        for arch in architectures:
            for root, dirs, files in walk("%(target)s/%(branch)s/%(arch)s" % locals()):
                for file in files:
                    if not path.islink("%(target)s/%(branch)s/%(arch)s/%(file)s" % locals()) and file.endswith(".xz"):
                        print("=> New Package: %(file)s" % locals())
                        print("    => Branch: %(branch)s" % locals())
                        print("    => Archictecture: %(arch)s" % locals())
                        newPackages.append(["%(target)s/%(branch)s/%(arch)s/%(file)s" % locals(), "%(target)s/%(branch)s/%(arch)s/%(file)s.sig" % locals()])
                        
    return newPackages

def verifyRepository(target, branches = ["winry-stable", "winry-testing"], architectures = ["i686", "x86_64"]):
    """Verify that the repository is suitable for upload"""

    print("=> Verifying repository...")

    safe = True

    #Make sure all the directories are present
    for branch in branches:
        if not path.isdir("%(target)s/%(branch)s" % locals()):
            print("    => Missing branch: %(branch)s" % locals())
            exit(1)

        for arch in architectures:
            if not path.isdir("%(target)s/%(branch)s/%(arch)s" % locals()):
                print("    => Missing Architecture: %(branch)s/%(arch)s" % locals())
                exit(1)

    #Make sure the files are safe
    for branch in branches:
        for arch in architectures:
            for root, dirs, files in walk("%(target)s/%(branch)s/%(arch)s" % locals()):
                for file in files:
                    if file.endswith(".xz") and "".join((file, ".sig")) not in listdir("%(target)s/%(branch)s/%(arch)s" % locals()):
                        print("    => No signature for package: %(file)s" % locals())
                        print("        => Branch: %(branch)s" % locals())
                        print("        => Archictecture: %(arch)s" % locals())
                        safe = False

                    if not file.endswith(".xz") and not file.endswith(".sig") and not file.endswith(".gz") \
                        and not file.endswith(".db") and not file.endswith(".files"):

                        print("    => Invalid file in cache: %(file)s" % locals())
                        print("        => Branch: %(branch)s" % locals())
                        print("        => Archictecture: %(arch)s" % locals())
                        safe = False

    #Make sure there directories are safe
    localBranches = listdir("%(target)s" % locals())

    for branch in localBranches:
        if branch not in branches and branch != "state" and branch != "lock" and branch != "pool":
            print("    => Invalid branch: %(branch)s" % locals())
            safe = False
            continue

        if branch == "state" or branch == "lock" or branch == "pool":
            continue

        localArchitectures = listdir("%(target)s/%(branch)s" % locals())

        for arch in localArchitectures:
            if arch not in architectures:
                print("    => Invalid Architecture: %(branch)s/%(arch)s" % locals())
                safe = False

    return safe
