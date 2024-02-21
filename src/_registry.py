from math import e
import os
import firebase_admin
from firebase_admin import credentials
from google.cloud.firestore import Client
from firebase_admin import firestore
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
    
    def addPackage(self, name:str, repo:str):
        self.key_value[name] = repo
    
    def getPackage(self, name:str):
        return self.key_value[name]
    
    def removePackage(self, name:str):
        self.key_value.pop(name)
    
    def write_to(self, file:str):
        lst = []
        for key, value in self.key_value:
            lst.append(f"{key}={value}")
        with open(file, "w+" if os.path.isfile(file) else "x+") as fwrite:
            fwrite.writelines(lst)
    
    def writeDefault(self):
        self.write_to(Registry.PATH_FILE)

def readPKMSourceFile(name:str) -> Registry:
    with open(name, "r+") as fread:
        lines = fread.readlines()
        return Registry.create_from_list(lines)
    
    
    
class PackagesRepo:
    def __init__(self) -> None:
        if not os.path.isfile(Registry.PATH_FILE):
            self.certificate = firebase_admin.initialize_app(firebase_admin.credentials.Certificate("./certificate.json"))
            self.client: Client = firestore.client()
            self.packages = self.client.collection("packages").document().get("packages_d").to_dict()
            if not self.packages:
                self.packages = {}
            self.packages_l: list[str] = self.packages["lspackages"]
            with open(Registry.PATH_FILE, "w") as fwrite:
                fwrite.writelines(self.packages_l)
            self.islocal = False
        else:
            with open(Registry.PATH_FILE, "r") as fread:
                self.packages_l = fread.readlines()
            self.islocal = True
        
    
    def getRegistry(self) -> Registry:
        reg = Registry.create_from_list(self.packages_l)
        return reg
    ...