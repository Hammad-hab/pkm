import typer
import subprocess as sb
from _registry import Registry
from _usrbase import Userbase
import os, tomli

PKMRC = \
"""
[pkm-repo]
creator={username}
name={pkgname}
repo={pkgrepo}
dinfo={pkgconcat}

[general]
version={pkgversion}
pack=true
"""

README = \
"""
# <INSERT_NAME>
version <INSERT_VERSION>
This is a sample README.md file that is meant to contain your package's documentation, information etc.

"""

class PackageCreator:
    def __init__(self) -> None:
        # Getting package name and version
        self.target_package_name = input("Enter Package Name: ")
        self.target_package_version = input("Enter Package Version: ")
        
        # Getting Username
        if os.path.isfile(Registry.PATH + "/" + "secrets.toml"):
            with open(Registry.PATH + "/" + "secrets.toml", "r") as f:
                contents = tomli.loads(f.read())
                self.user = contents["contents"]["username"]
        else:
            print("You don't seemed to be logged in, please login")
            base = Userbase(record=True, ignore_record=False)
            base.login(terminal_mode=True)
            self.user = base.pusername
            
        print("REPO Initialization disabled, you need to connect to an existing repo")
        self.github_remote_url = input("Enter Github URL: ")
        if self.github_remote_url:
            sb.run(["sudo", "git", "remote", "add", "origin", self.github_remote_url])
            sb.run(["sudo", "git", "branch", "-M", "main"])
        else:
            self.init_repo = typer.confirm("Initialize github repository? ")
            sb.run(["sudo", "git", "init"])
        
        os.mkdir(self.target_package_name)
        os.chdir(self.target_package_name)
        os.mkdir("src")
        with open(".pkmrc", "w") as fwrite:
            fwrite.write(PKMRC.format(username=self.user, pkgname=self.target_package_name, pkgrepo=self.github_remote_url, pkgconcat=self.target_package_name + self.github_remote_url, pkgversion=self.target_package_version))
        with open("README.md", "w") as fwrite:
            fwrite.write(README)
        os.chdir("src")
        with open("__init__.🔥", "w") as f:
            f.write("fn main() raises:\n\tprint(\"Hello from pkm!\")")
        os.chdir("../")
        os.mkdir("setupfiles")
        os.chdir("setupfiles")
        with open("__pkm_setup__.🔥", "w") as f:
            f.write(f"\"\"\"\nThis file will be executed when a package is installed\n\"\"\"fn main() raises:\n\tprint(\"Setting up {self.target_package_name}!\")")
        with open("__pkm_purge__.🔥", "w") as f:
            f.write(f"\"\"\"\nThis file will be executed when a package is installed\n\"\"\"fn main() raises:\n\tprint(\"Purging up {self.target_package_name}!\")") 
          
        pass
    ...