from genericpath import isfile
import typer, os, shutil
from _utils import CONFIG, warn, console, abort, color, success
from _app import PKMManager, readPKMSourceFile, Registry, PackagesRepo
from _http import PKMGitClone
from _usrbase import Userbase
app = typer.Typer()


@app.command()
def install(package_name: str, disable_logs:bool=False, pack:bool=True):
    """
    Install a mojo package. You can disable logs by setting disable_logs=True
    If you want a folder instead of a .📦 you can disable pack (not recommended)
    """
    CONFIG["en-logs"] = not disable_logs
    CONFIG["pack-package"] = pack
    if not pack:
        warn(
            "Disabling pack means that the installed package will not be compiled to a .📦 (.mojopkg)" \
            " which could be inefficient are you sure you want to do this?"
        )
    manager = PKMManager()
    manager.fetchPackage(package_name)
    
@app.command()
def purge(package_name: str, disable_logs:bool=False, ):
    """
    Delete (purge) a package from your system. You can disable logs by setting disable_logs=True.
    """
    
    CONFIG["en-logs"] = not disable_logs
    if PKMManager.hasInstalledPackage(package_name):
        delpackage = typer.confirm(color(f"Are you sure you want to delete {package_name}?", color="yellow"))
        if not delpackage:
            raise typer.Abort()
        warn(f"Deleting {package_name}...")
        if os.path.isfile(PKMGitClone._MND_DIR + package_name + ".mojo"):
            os.remove(PKMGitClone._MND_DIR + package_name + ".mojopkg")
        elif os.path.isdir(PKMGitClone._MND_DIR + package_name):
            shutil.rmtree(PKMGitClone._MND_DIR + package_name)
        else:
            abort(f"Could not track any package named {package_name}", "Purging package")
        success(f"Successfully deleted package {package_name}")
        installed_reg = readPKMSourceFile(Registry.INSTALLED_FILE)
        installed_reg.removePackage(package_name)
        installed_reg.write_to(Registry.INSTALLED_FILE)
        success(f"Successfully updated package registry {Registry.INSTALLED_FILE}")
        
    else:
        abort("User tried to purge a package that hasn't been instaled", "Purging a package")
        
@app.command()
def upload(record_creds:bool=True, ignore_stored:bool=False):
    """
        Upload a package to pkm repository.\n
        record_creds (True/False): specify if you want to prevent pkm from storing your credentials to prevent you from 
        having to login every time you upload a package\n
        ignore_stored (True/False): specify if you forcefully want pkm to ignore recorded credentials. This is useful if you want
        to login again.
    """
    base = Userbase(record=record_creds, ignore_record=ignore_stored)
    base.login(terminal_mode=True)
    base.uploadPackage(terminal_mode=True)
    # abort("Command not supported yet...work in progress.")

@app.command()
def has(package_name: str):
    "Check if a package has been installed"
    console.print(PKMManager.hasInstalledPackage(package_name))
    
@app.command()
def config():
    "Print the default Configuration"
    console.print_json(data=CONFIG)

@app.command()
def update():
    "Reload the registry i.e fetch new packages"
    try:
        pk = PackagesRepo(True)
        success("Successfully updated sources.list")
    except Exception as e:
        abort(f"Failed to update sources.list because of an internal error: {e!r}", "Updating sources.list")

@app.command()
def create():
    "Create an account on pkm repository index"
    base = Userbase()
    username = input("Username: ")
    password = input("Password: ")
    base.create_account(username, password)
   
