#!/usr/bin/bash

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

echo "Installing Pinako..."

#Make sure in pinako directory

if [[ ! -d "data" ]] || [[ ! -d "pinako" ]]; then
    echo "Not a valid pinako directory"
    exit 1
fi

if [[ -d "/usr/share/pinako" ]] || [[ -f "/usr/bin/pinako" ]]; then
    echo "Pinako already installed"
    exit 1
fi

mkdir -p "/usr/bin"
mkdir -p "/usr/share/pinako"
mkdir -p "/usr/share/pinako/data"

cp -r pinako/* /usr/share/pinako/
cp -r data /usr/share/pinako
mv /usr/share/pinako/pinako /usr/bin/pinako

chmod +x /usr/bin/pinako
chmod +x /usr/share/pinako/pinako.py
