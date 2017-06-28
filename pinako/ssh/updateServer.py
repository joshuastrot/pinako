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

def updateServer(sshClient, packagerName, packagerEmail, branches = ["winry-stable", "winry-testing"]):
    """Update the server with new repository"""

    #Lock the database
    sshClient.lockServer(packagerName, packagerEmail)

    #Upload the archive
    print("=> Uploading new pinako archive")
    sshClient.up("/tmp/pinako-upload.tar", "/srv/http/pinako-upload.tar")

    #Clear the Server
    print("=> Deleting old repository")
    for branch in branches:
        sshClient.runCommand("rm -r /srv/http/%(branch)s" % locals())

    #Update state file
    print("=> Updating state file")
    sshClient.runCommand("rm /srv/http/state")

    #Extract the archive
    print("=> Extracting archive on server")
    sshClient.runCommand("tar -xf /srv/http/pinako-upload.tar -C /srv/http")

    #Remove the archive
    print("=> Removing server archive")
    sshClient.runCommand("rm /srv/http/pinako-upload.tar")

    #Unlock the Server
    sshClient.unlockServer()
