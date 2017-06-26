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

import paramiko

from getpass import getpass

def retrieveSSHPassword():
    """Retrieve the SSH password to unlock the ssh key"""

    print("=> Please enter your SSH password")
    password = getpass()

    return password

def connect(sshUsername, sshAddress, sshKey):
    """Connect to a ssh server and return a client"""

    print("=> Connecting over SSH to: %(sshAddress)s" % locals())

    sshPassword = retrieveSSHPassword()

    sshKeyUnlocked = paramiko.RSAKey.from_private_key_file(sshKey, password = sshPassword)
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(sshAddress, username = sshUsername, pkey = sshKeyUnlocked)

    return sshClient

def runCommand(sshClient, command):
    """Run a command over ssh and return the output"""

    (stdin, stdout, stderr) = sshClient.exec_command(command)

    return [stdin, stdout, stderr]
