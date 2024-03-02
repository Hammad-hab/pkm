
"""

    TODO: Add code to help support package uploading process
    
"""
from _utils import getFirestoreDocumentRaw, abort, success, errmsg
from _registry import Registry
from google.cloud.firestore import ArrayUnion, ArrayRemove
import re
from validators import url as isURL
import typer
from termcolor import colored as color
from tomli import loads
import os

class Userbase:
    
    @staticmethod
    def isInvalid(thing:str, what):
        if what == "name":
            return False if not re.search("[A-Z]|\s", thing) else True
        elif what == "repo":
            return False if not re.search("\s", thing) and isURL(thing) else True
        else:
            abort(f"Internal process failure at Userbase.isInvalid INV-MODE {what}", "running cogs")
            
        
    def __init__(self, record=False, ignore_record=True) -> None:
        self.users_db_pointer = getFirestoreDocumentRaw("users")
        self.lspackages_db_pointer = getFirestoreDocumentRaw("packages_d")
        self.target_metadata = {}
        self.record=record
        self.ignore_record=ignore_record
        pass
    
    def create_account(self, username:str="", password:str="", record=False):
        self.users_db_pointer.update({
            f'{username}': {
                'password': password,
                'hasAccessTo': []
            }
        })
        if record:
            with open(Registry.PATH + "/secrets.toml", "w") as f:
                    f.write(
                        "[credentials]\n"\
                        f"username=\"{username}\"\n"\
                        f"password=\"{password}\""
                        )
    
    def login(self, terminal_mode=False, username:str="", password:str="") -> None:
        if self.ignore_record or not os.path.isfile(Registry.PATH + "/secrets.toml"):
            self.pusername = username if not terminal_mode else input("Username: ")
            self.ppassword = password if not terminal_mode else input("Password: ")
        elif not self.ignore_record:
    
            with open(Registry.PATH + "/secrets.toml") as f:
                secrets = loads(f.read())
                self.pusername = secrets["credentials"]["username"]
                self.ppassword = secrets["credentials"]["password"]
        
        INSTANCE = self.users_db_pointer.get().to_dict()
        if self.pusername not in INSTANCE.keys():
            abort(f"No user named {self.pusername} could be found. Is it possible that there was a typo?", "Logging in")
            return
        
        if self.ppassword != INSTANCE[self.pusername]["password"]:
            abort("Invalid credentials!", "Logging in")
            return
        INSTANCE: dict = INSTANCE[self.pusername]
        INSTANCE.pop("password")
        self.target_metadata = INSTANCE
        if self.record:
            with open(Registry.PATH + "/secrets.toml", "w") as f:
                f.write(
                    "[credentials]\n"\
                    f"username=\"{self.pusername}\"\n"\
                    f"password=\"{self.ppassword}\""
                    )

    def getLoggedInUser(self):
        return self.pusername
    
    def getUserAccessablePackages(self):
        return self.target_metadata["hasAccessTo"]
    
    def uploadPackage(self, package_name:str="", repository:str="", terminal_mode=False):
        # if not self.getLoggedInUser():
        #     abort("User not logged in", "Initiating upload process")
        name = package_name if not terminal_mode else input("Name of package [Must not contain spaces and/or capital letters] ").strip()
        if Userbase.isInvalid(name, "name"):
            errmsg("Invalid package name...RSTART")
            print("---RESTART---")
            self.uploadPackage()
        repo = repository if not terminal_mode else input("URL of package [Github repository] ").strip()
        if Userbase.isInvalid(repo, "repo"):
            errmsg("Invalid repository URL...RSTART")
            print("---RESTART---")
            self.uploadPackage()
            
        INCLUDED = f'{name}={repo}' in self.lspackages_db_pointer.get().to_dict()["lspackages"]
        HAS_ACCESS = f'{name}={repo}' in self.users_db_pointer.get().to_dict()[self.pusername]["hasAccessTo"]
        if not INCLUDED:
            self.lspackages_db_pointer.update({
                "lspackages": ArrayUnion([f'{name}={repo}'])
            })
            LCopy = self.users_db_pointer.get().to_dict()[self.pusername]
            LCopy["hasAccessTo"].append(f'{name}={repo}')
            self.users_db_pointer.update({
                f'{self.pusername}': LCopy
            })
            # Package is not uploaded yet, upload safe.
            pass
        elif INCLUDED and HAS_ACCESS:
            """
                TODO: add INCLUDED and HAS_ACCESS support
            """
            abort("INCLUDED and HAS_ACCESS is disabled because of certain bugs....", "Uploading")
            override = typer.confirm(color(f"{name} already exists in the registry, are you sure you want to override metadata?", color="yellow"))
            if not override:
                abort("Upload aborted by user....")
            
            # Package exists but the user has authorization to override it
            pass
        elif INCLUDED and not HAS_ACCESS:
            abort(f"{name} already exists in registry and you do not have authorization to override it")
            # Package exists and the USER DOES NOT have authorization to override it
            pass
        success("Successfully uploaded pacakge metadata to registry. Now you can just commit to your repository and the updates will automatically be captured. You not need re-upload the package.")
        success("Successfully updated Access-Variables")