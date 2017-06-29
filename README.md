Pinako
======
Pinako is a client to communicate over SSH and SFTP with a Winry Linux server. It initializes a client side repository, allows you to make yours changes to it, and then pushes it up to a server. There's many different features that make this easier, such as:

* Moves all packages to a pool and utilizes symbolic links to save space
* Ability to lock and unlock server so other packagers don't push at the same time
* Branch management to compare and merge branches
* Tracking to determine changes on local repository versus remote
* Performs sanity checks on the local repository before pushing to make sure it is safe
* Uses a configuration file to make customization of Pinako settings easy

Installation
============
Anyone can install Pinako, but only verified packagers may use it on a Winry Linux server.

Dependencies
------------
```
python
python-paramiko
python-yaml
```

Winry Linux
-----------
On Winry, Pinako can be installed with `pacman`
```bash
sudo pacman -S pinako
```

All Other Linux
---------------
On any other linux operating systems, it will have to be installed manually.
```bash
git clone https://github.com/winry-linux/pinako.git ~/pinako
cd ~/pinako
sudo bash install.sh
```

Usage
=====
To display a help menu for Pinako, simply run Pinako
```bash
pinako
```

Configuring
===========
Pinako will not run without a configuration file for the user. To create one, copy it from `/usr/share/pinako/data/pinako.yaml` to `~/.config/pinako/pinako.yaml`
```bash
mkdir -p ~/.config/pinako
cp /usr/share/pinako/data/pinako.yaml ~/.config/pinako/pinako.yaml
```
You can then configure the file for your user. An example configuration would look like:
```yaml
Cache: /home/john/repository
PackagerEmail: johndoe@gmail.com
PackagerName: John Doe
SSHKey: /home/john/.ssh/id_rsa
ServerAddress: johndoerepo.org
Username: john
```

Authors
=======
* Joshua Strot <joshua@winrylinux.org>

License
=======
This project is licensed under the GNU General Public License. See [LICENSE](LICENSE) for more details.
