import firebase_admin, sys
from google.cloud.firestore import Client, CollectionReference
from firebase_admin import firestore
from math import inf
from typing import Any, Callable, Iterable
from termcolor import colored as color
from rich.console import Console
from git import RemoteProgress
from Levenshtein import distance
import os

console = Console()
class FNCallOnce:
    def __init__(self, function:Callable) -> None:
        self.fnbind = function
        self.hasBeenCalled = False
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self.hasBeenCalled:
            self.hasBeenCalled = True
            return self.fnbind(*args, **kwds)
        else:
            raise Exception("Function (FNCallOnce Wrapper) has already been called")

CONFIG = {
    "en-logs": True,
    "pack-package": True
}

def strict_one_call(wrapper:Callable):
    return FNCallOnce(wrapper)

def abort(err:str, process:str):
    print(color(color="red",text=
        f"Error while attempting to {process}\n\t" \
        f"{err}\n\tExiting with code -1" 
    ))
    exit(-1)

def errmsg(err:str):
    print(color(color="red",text=
        f"ERROR: {err}"
    ))



def info(info:str):
    if not CONFIG["en-logs"]:
        return None
    print(color(color="light_blue",text=
        f"INFO: {info}" 
    ))

def success(message:str):
    if not CONFIG["en-logs"]:
        return None
    print(color(color="light_green",text=
        f"SUCCESS: {message}" 
    ))

def warn(message:str):
    if not CONFIG["en-logs"]:
        return None
    print(color(color="yellow",text=
        f"WARNING: {message}" 
    ))
    
class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if max_count is not None:
            completed = int(cur_count / max_count * 50)  # Using 50 characters for the progress bar #type:ignore
            remaining = 50 - completed
            progress_bar = "[%s%s]" % ('▓' * completed, '░' * remaining)
            sys.stdout.write("\r%s" % progress_bar)
            sys.stdout.flush()
        else:
            sys.stdout.write("\r[%s]" % ('▓' * int(cur_count / 10))) #type:ignore
            sys.stdout.flush()
        sys.stdout.write(" %s" % message)
        sys.stdout.flush()
    
        
def generate_compile_command(compile="_main.py", includes=[]):
    command = f"pyinstaller --onefile "
    with open("requirements.txt", 'r') as f:
        for line in f.readlines():
            package = line.split("==")[0]
            if package not in includes:
                command += f" --exclude-module={package}"
            else:
                command += f" --hidden-import={package}"
    return command + " " + compile
    ...

def findNearest(target:str, from_:Iterable[str]):
    smallest = inf
    smallest_l_string = None
    for string in from_:
        dist = distance(target, string)
        if distance(target, string) < smallest:
            smallest = dist
            smallest_l_string = string
    return smallest_l_string

script_dir = os.path.dirname(os.path.abspath(__file__))
certificate_path = os.path.join(script_dir, "certificate.json")

CERTIFICATE = firebase_admin.initialize_app(firebase_admin.credentials.Certificate(certificate_path))
CLIENT: Client = firestore.client()

def getCollection(name:str) -> CollectionReference:
    return CLIENT.collection(name)

packages: CollectionReference = getCollection("packages")

def getFirestoreDocument(name) -> dict:
    dat = packages.document(name).get().to_dict()
    return {} if not dat else dat

def setFirestoreDocument(name, data) -> None:
    dat = packages.document(name).set(data)

def setFirestoreDocumentM(name, data) -> None:
    dat = packages.document(name).set(data, merge=True)
    
