from typing import Any, Callable
from termcolor import colored as color
from rich.progress import Progress as progress
from git import RemoteProgress
import sys
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


def strict_one_call(wrapper:Callable):
    return FNCallOnce(wrapper)

def abort(err:str, process:str):
    print(color(color="red",text=
        f"Error while attempting to {process}\n\t:" \
        f"{err}\n\tExiting with code -1" 
    ))
    exit(-1)


def info(info:str):
    print(color(color="light_blue",text=
        f"INFO: {info}" 
    ))

def success(message:str):
    print(color(color="light_green",text=
        f"SUCCESS: {message}" 
    ))

def warn(message:str):
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