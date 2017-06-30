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

import paramiko

from getpass import getpass
from datetime import datetime

def retrieveSSHPassword():
    """Retrieve the SSH password to unlock the ssh key"""

    print("    => Please enter your SSH password")
    password = getpass("    => Password: ")

    return password

class sshClient():
    """Client to perform ssh operations"""

    def __init__(self, sshUsername, sshAddress, sshKey):
        """Initialize the SSH Client"""

        print("=> Connecting over SSH to: %(sshAddress)s" % locals())

        sshPassword = retrieveSSHPassword()

        sshKeyUnlocked = paramiko.RSAKey.from_private_key_file(sshKey, password = sshPassword)
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshClient.connect(sshAddress, username = sshUsername, pkey = sshKeyUnlocked)

        self.scpClient = self.sshClient.open_sftp()

    def runCommand(self, command):
        """Run a command over ssh and return the output"""

        (stdin, stdout, stderr) = self.sshClient.exec_command(command)

        return [stdin, stdout, stderr]

    def down(self, localPath, remotePath):
        """Download a file from the remote host"""
        self.scpClient.get(remotePath, localPath)

    def up(self, localPath, remotePath):
        """Upload a file from the remote host"""
        self.scpClient.put(localPath, remotePath)

    def lockServer(self, packagerName, packagerEmail, serverPath):
        """Lock the server to perform uploads"""
        print("=> Locking the server")

        (stdin, stdout, stderr) = self.runCommand("cat %(serverPath)s/lock" % locals())
        if stdout and not stderr:
            print("=> Error! Database is already locked. Information:")
            for line in stdout.readlines():
                print(line.strip())
            exit(1)

        try:
            with open("/tmp/lock", "w") as lock:
                time = datetime.now().time()
                lock.write("The database has been locked for uploading.\n\nPackager: %(packagerName)s\nPackagerEmail: %(packagerEmail)s\nTime: %(time)s" % locals())
        except IOError as e:
            print("=> Could not create a lock file.")
            exit(1)

        self.up("/tmp/lock", "%(serverPath)s/lock" % locals())

    def unlockServer(self, serverPath):
        """Unlock the server"""
        print("=> Unlocking the server")

        self.runCommand("rm %(serverPath)s/lock" % locals())
