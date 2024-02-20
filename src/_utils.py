from typing import Any, Callable, Generic, TypeVar
from termcolor import colored as color

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

@strict_one_call
def abort(err:str, process:str):
    print(color(color="white", on_color="on_red",text=
        f"Error while attempting to {process}\n\t:" \
        f"{err}\n\tExiting with code -1" 
    ))
    exit(-1)