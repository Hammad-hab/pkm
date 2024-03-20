from math import e
import os
from _utils import success, getFirestoreDocument
import os

class Registry:
    PATH = "/Users/Shared/mojo_pkm"
    PATH_FILE = "/Users/Shared/mojo_pkm/sources.list"
    INSTALLED_FILE = "/Users/Shared/mojo_pkm/installed.list"
    """
        A data structure designed to contain package name and their respective
        get URL.
    """
    
    @classmethod
    def create_from_list(cls, list:list[str]):
        instance = cls()
        for item in list:
            name, repo = item.split("=")
            instance.addPackage(name, repo)
        return instance
        ...
    
    def __init__(self) -> None:
        self.key_value = {}
    
    def hasPackage(self, pacakge_name:str):
        return pacakge_name in self.key_value.keys()
        ...
    
    def addPackage(self, name:str, repo_or_version:str):
        self.key_value[name] = repo_or_version
    
    def getPackage(self, name:str):
        return self.key_value[name]
    
    def removePackage(self, name:str):
        self.key_value.pop(name)
    
    def write_to(self, file:str):
        lst = []
        for key, value in self.key_value.items():
            lst.append(f"{key}={value}")
        with open(file, "w+" if os.path.isfile(file) else "x+") as fwrite:
            fwrite.writelines(x + '\n' for x in lst)
    
    def writeDefault(self):
        self.write_to(Registry.PATH_FILE)

def readPKMSourceFile(name:str, retlist=False) -> Registry | list[str]:
    if not os.path.isfile(name):
        with open(name, "x+") as fread:
            return Registry()
    with open(name, "r+") as fread:
        lines = fread.readlines()
        lines = [ln.replace("\n", '') for ln in lines]
        if retlist:
            return lines
        return Registry.create_from_list(lines)
    
    
"""
    FIXME:
        * Bugfix: force_reload mechanism is buggy and might caus problems
"""
class PackagesRepo:
    def __init__(self, force_reload=False) -> None:
        if (not os.path.isfile(Registry.PATH_FILE)) or (force_reload):
            self.packages =getFirestoreDocument("packages_d")
            if not self.packages:
                self.packages = {}
            self.packages_l: list[str] = self.packages["lspackages"]
            with open(Registry.PATH_FILE, "w") as fwrite:
                fwrite.writelines([x + '\n' for x in self.packages_l])
            self.islocal = False
            if force_reload:
                success("Fetched new packages from Registry.")
        else:
            with open(Registry.PATH_FILE, "r") as fread:
                self.packages_l = fread.readlines()
                self.packages_l = [ln.replace("\n", '') for ln in self.packages_l]
                
            self.islocal = True
        
    
    def getRegistry(self) -> Registry:
        reg = Registry.create_from_list(self.packages_l)
        return reg
    ...