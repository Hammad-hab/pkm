#INSTALLER<INSERT_PYTHON_PATH>
from _command import app
from extends import EXTENSIONS

EXTENSIONS["on_app_start"]

if __name__ == "__main__":
    EXTENSIONS["on_before_start"]
    app()
    EXTENSIONS["on_after_start"]
    
    
EXTENSIONS["on_app_end"]
    