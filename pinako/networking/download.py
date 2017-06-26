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

import urllib.request

from os import makedirs

def databases(path, configuration):
    """Download the databases"""

    print("=> Downloading databases")

    #Download the databases
    databases = []
    for branch in configuration["Branches"]:
        print("=> [%(branch)s] Grabbing package databases" % locals())

        print("    => [%(branch)s] Downloading i686 database" % locals())
        urllib.request.urlretrieve("".join((configuration["URL"], "/winry-", branch, "/i686/winry-", branch, ".db")), \
            "".join(("/tmp/winry-", branch, "-i686.db"))
        )
        databases.append("".join(("/tmp/winry-", branch, "-i686.db")))

        print("    => [%(branch)s] Downloading x86_64 database" % locals())
        urllib.request.urlretrieve("".join((configuration["URL"], "/winry-", branch, "/x86_64/winry-", branch, ".db")), \
            "".join(("/tmp/winry-", branch, "-x86_64.db"))
        )
        databases.append("".join(("/tmp/winry-", branch, "-i686.db")))

    return databases
