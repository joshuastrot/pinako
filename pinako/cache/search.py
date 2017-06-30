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

from os import path, walk, listdir

def regular(target, branches = ["winry-stable", "winry-testing"]):
    """Check the cache for regular, non database files"""

    print("=> Searching local database for additions")

    newPackages = []
    for branch in branches:
        for root, dirs, files in walk("%(target)s/%(branch)s" % locals()):
            for file in files:
                if not path.islink("%(target)s/%(branch)s/%(file)s" % locals()) and file.endswith(".xz"):
                    print("=> New Package: %(file)s" % locals())
                    print("    => Branch: %(branch)s" % locals())
                    newPackages.append(["%(target)s/%(branch)s/%(file)s" % locals(), "%(target)s/%(branch)s/%(file)s.sig" % locals()])

    if not newPackages:
        print("    => Nothing appears to have changed locally.")

    return newPackages

def verifyRepository(target, branches = ["winry-stable", "winry-testing"]):
    """Verify that the repository is suitable for upload"""

    print("=> Verifying repository...")

    safe = True

    #Make sure all the directories are present
    for branch in branches:
        if not path.isdir("%(target)s/%(branch)s" % locals()):
            print("    => Missing branch: %(branch)s" % locals())
            exit(1)

    #Make sure the files are safe
    for branch in branches:
        for root, dirs, files in walk("%(target)s/%(branch)s" % locals()):
            for file in files:
                if file.endswith(".xz") and "".join((file, ".sig")) not in listdir("%(target)s/%(branch)s" % locals()):
                    print("    => No signature for package: %(file)s" % locals())
                    print("        => Branch: %(branch)s" % locals())
                    safe = False

                if not file.endswith(".xz") and not file.endswith(".sig") and not file.endswith(".gz") \
                    and not file.endswith(".db") and not file.endswith(".files") and file != ".htaccess":

                    print("    => Invalid file in cache: %(file)s" % locals())
                    print("        => Branch: %(branch)s" % locals())
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

    if not safe:
        print("=> Repository is not safe!")
        exit(1)
    else:
        print("=> Repository appears safe. Use your best judgement though.")

    return safe

def compareBranches(target, branches, confBranches=["winry-stable", "winry-testing"]):
    """Compare to branches for differences"""

    #Assign these variables for convenience
    sourceBranch = branches[0]
    targetBranch = branches[1]

    print("=> Comparing %(sourceBranch)s -> %(targetBranch)s" % locals())

    #Validate the given branches
    for branch in branches:
        if branch not in confBranches:
            print("=> Error! Branch %(branch)s not a real branch." % locals())
            exit(1)

    #Grab relevent files from branches
    sourceBranchContents = listdir("%(target)s/%(sourceBranch)s" % locals())
    sourceBranchContents = [pack for pack in sourceBranchContents if pack.endswith(".xz")]
    targetBranchContents = listdir("%(target)s/%(targetBranch)s" % locals())
    targetBranchContents = [pack for pack in targetBranchContents if pack.endswith(".xz")]

    #Iterate over and find additions or removals
    additions = [pack for pack in sourceBranchContents if pack not in targetBranchContents]
    removals = [pack for pack in targetBranchContents if pack not in sourceBranchContents]

    #Print the results
    if additions:
        for package in additions:
            print("    => Package added in %(sourceBranch)s: %(package)s" % locals())
    else:
        print("    => No new additions to %(sourceBranch)s" % locals())

    if removals:
        for package in removals:
            print("    => Package removed in %(sourceBranch)s: %(package)s" % locals())
    else:
        print("    => No removals in %(sourceBranch)s" % locals())

    return [additions, removals]
