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

def updateServer(sshClient, packagerName, packagerEmail, serverPath, branches = ["winry-stable", "winry-testing"]):
    """Update the server with new repository"""

    #Lock the database
    sshClient.lockServer(packagerName, packagerEmail, serverPath)

    #Upload the archive
    print("=> Uploading new pinako archive")
    sshClient.up("/tmp/pinako-upload.tar", "%(serverPath)s/pinako-upload.tar" % locals())

    #Clear the Server
    print("=> Deleting old repository")
    for branch in branches:
        sshClient.runCommand("rm -r %(serverPath)s/%(branch)s" % locals())

    sshClient.runCommand("rm -r %(serverPath)s/pool" % locals())
    sshClient.runCommand("rm %(serverPath)s/state" % locals())

    #Extract the archive
    print("=> Extracting archive on server")
    sshClient.runCommand("tar -xf %(serverPath)s/pinako-upload.tar -C %(serverPath)s" % locals())

    #Remove the archive
    print("=> Removing server archive")
    sshClient.runCommand("rm %(serverPath)s/pinako-upload.tar" % locals())

    #Unlock the Server
    sshClient.unlockServer(serverPath)
