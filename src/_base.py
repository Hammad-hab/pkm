import firebase_admin
from firebase_admin import credentials
from google.cloud.firestore import Client
from firebase_admin import firestore
import os
from _utils import strict_one_call, abort
import git
import shutil

class MIPInit:
    
    __PATH = "/Users/Shared/mojo_pkm"
    __PATH_FILE = "/Users/Shared/mojo_pkm/sources.list"
    __FBAPP = firebase_admin.initialize_app(firebase_admin.credentials.Certificate("./certificate.json"))
    
    @staticmethod
    @strict_one_call
    def getPackages() -> dict[str, str]:
        db = firestore.client()
        
        dbref: Client = db.collection("packages")
        df = dbref.document("packages_d").get().to_dict()
        return df if df is not None else {}
        
    def __init__(self) -> None:
        
        if not os.path.isfile(MIPInit.__PATH_FILE):
            if not os.path.isdir(MIPInit.__PATH):
                os.mkdir(MIPInit.__PATH)
            self.packages = MIPInit.getPackages()["lspackages"]
            initial_dir = os.getcwd()
            os.chdir(MIPInit.__PATH)
            with open(MIPInit.__PATH_FILE, "+x") as fwrite:
                fwrite.writelines(self.packages)
            os.chdir(initial_dir)
        else:
            with open(MIPInit.__PATH_FILE, "r") as fread:
                self.packages = fread.readlines()
        
        pass

    def registryHasPackage(self, name:str):
        indexPackage = 0
        for package in self.packages:
            name_target = package.split("=")[0]
            if name == name_target:
                return (True, indexPackage)
            indexPackage += 1
        return (False, indexPackage)

    def fetchPackage(self, name:str):
        registryInstance = self.registryHasPackage(name)
        if not name or not registryInstance[0]:
            abort(f"Package {name} not found", "Fetching package")
        
        if not os.path.isdir("mojo_modules"):
            os.mkdir("./mojo_modules")
        Package = self.packages[0].split("=")
        os.chdir("./mojo_modules")
        repo = git.Repo.clone_from(Package[1], "tmp")
        shutil.move("tmp/"+Package[0], "./")
        shutil.rmtree("tmp")
            

mip = MIPInit()
mip.fetchPackage("stdlib_extensions")