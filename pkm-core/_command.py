import typer, os, shutil, tomli
from _utils import CONFIG, warn, console, abort, color, success, findNearest
from _utils import info as info_
from _app import PKMManager, readPKMSourceFile, Registry, PackagesRepo
from _http import PKMGitClone
from _usrbase import Userbase
import subprocess as sb
from _pkgcreator import PackageCreator


try:
    import tkinter as tk
    SUPPORT_TK = True
except:
    SUPPORT_TK = False
    
    warn("--gui will not work in pkm listpkgs because your python version does not have it")

app = typer.Typer(name="pkm", )

@app.command()
def info():
    print(CONFIG["information"])
@app.command()
def install(
        package_name: str, 
        disable_logs:bool=False, 
        pack:bool=True
    ):
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
def purge(
        package_name: str, 
        disable_logs:bool=False, 
        force:bool=typer.Option(help="Forcefully delete a package, no questions asked.",default=False)
    ):
    """
    Delete (purge) a package from your system. You can disable logs by setting disable_logs=True.
    """
    
    CONFIG["en-logs"] = not disable_logs
    if PKMManager.hasInstalledPackage(package_name):
        delpackage = typer.confirm(color(f"Are you sure you want to delete {package_name}?", color="yellow")) if not force else True
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
    print("Scanning For a potential package...")
    base = Userbase(record=record_creds, ignore_record=ignore_stored)
    base.login(terminal_mode=True)
    if os.path.isfile(".pkmrc"):
        success("Found a package (.pkmrc)! Automatically uploading project....")
        with open(".pkmrc", "r") as rc:
            contents = tomli.loads(rc.read())
            contents["pkm-repo"]
            base.uploadPackage(name=contents["pkm-repo"]["name"], repository=contents["pkm-repo"]["repo"], version=contents["general"]["version"])
        ...
    else:
        warn(".pkmrc not found, switching to TERMINAL_MODE")
        base.uploadPackage(terminal_mode=True)
    # abort("Command not supported yet...work in progress.")


@app.command()
def has(package_name: str):
    """Check if a package has been installed"""
    console.print(PKMManager.hasInstalledPackage(package_name))
    
@app.command()
def config():
    """Print the default Configuration"""
    console.print_json(data=CONFIG)

@app.command()
def update():
    """Reload the registry i.e fetch new packages"""
    try:
        pk = PackagesRepo(True)
        success("Successfully updated sources.list")
    except Exception as e:
        raise
        abort(f"Failed to update sources.list because of an internal error: {e!r}", "Updating sources.list")

@app.command()
def create(
        what:str, 
        autologin:bool=typer.Option(help="Automatically login after creating account. Works if what=account", default=False)
    ):
    """Create an account on pkm repository index\n
    what: string = account OR package
    """
    if what != "account" and what != "package": 
        abort(f"Invalid value for what, {what}. Did you instead mean {findNearest(what, ['account', 'package'])}?", "Creating account/package")
    
    if what == "account":
        base = Userbase()
        username = input("Username: ")
        password = input("Password: ")
        base.create_account(username, password, autologin)
    elif what == "package":
        print("Creating package...")
        pkgcreator = PackageCreator()
            
        ...
    
@app.command()
def delete(
        force:bool=typer.Option(help="Forcefully delete pkm, no questions asked 😉", default=False), 
        silent:bool=typer.Option(help="Silence the logs, only recieve error messages 🤫", default=False)
    ):
    """Uninstall pkm"""
    CONFIG["en-logs"] = False if silent else True
    
        
    delete = typer.confirm(color(f"Are you sure you want to delete pkm? (Packages won't be deleted unless explicity specified)", color="yellow")) if not force else True
    if not delete:
        raise typer.Abort()
    
    print("Uninstalling pkm...")
    info_("Performing checkups...")
    if os.path.isdir("/usr/local/bin/pkmd") and os.path.isfile("/usr/local/bin/pkm"):
        info_("Deleting pkmd, admin privileges REQUIRED!")
        try:
            shutil.rmtree("/usr/local/bin/pkmd")
        except:
            abort("Could not delete pkmd from system", "Deleting pkmd directory")
        else:
            success("Successfully removed pkmd. Proceeding to obliterate pkm.sh")
        
        try:
            os.remove("/usr/local/bin/pkm")
        except:
            abort("Could not delete /usr/local/bin/pkm.sh", "Deleting pkm script")
        else:
            success("Successfully removed pkm.sh")
            info_(f"Goodbye {CONFIG['usname']}!")
        ...
    else:
        abort("Could not track pkm cli and pkmd source. This can happen if the pkm cli was moved from it's original position.", "Deleting pkm")

@app.command()
def listpkgs(
    gui:bool=typer.Option(help="Display all the available packages in a GUI list instead of the terminal", default=False), 
):
    """
    Lists all the available packages
    """
    packages: list[str] = readPKMSourceFile(Registry.PATH_FILE, True)
    if gui and SUPPORT_TK:
        root = tk.Tk()
        root.title("PKM packages")
        root.resizable(0,0)
        # root.geometry("250x200")
        LIST = tk.Listbox(root)
        i = 0
        for package in packages:
            package = package.split("=")
            LIST.insert(i, package[0])
            i += 1
        
        # LIST.bind("<Double-1>", lambda x: root.clipboard_append(packages[LIST.curselection()[0]].split("=")[0]))
        def clipboard_write():
            root.clipboard_clear()
            item = LIST.curselection()[0]
            item_name = packages[item].split("=")[0]
            root.clipboard_append(item_name)
        LIST.bind("<Double-1>", lambda x: clipboard_write())
        LIST.focus()
        LIST.pack(padx=10, pady=10,)
        root.mainloop()
    else:
        for package in packages:
            print(package)