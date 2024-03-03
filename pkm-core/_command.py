import typer, os, shutil
from _utils import CONFIG, warn, console, abort, color, success, findNearest
from _utils import info as info_
from _app import PKMManager, readPKMSourceFile, Registry, PackagesRepo
from _http import PKMGitClone
from _usrbase import Userbase
import subprocess as sb
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
    base = Userbase(record=record_creds, ignore_record=ignore_stored)
    base.login(terminal_mode=True)
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
        package_name = input("Name of Package: ")
        make_repo = typer.confirm("Initalize git repository?")
        if not make_repo:
            connect_repo = typer.confirm("Connect to existing git repository?")
            if connect_repo:
                repo_name = input("Repo URL:")
        # make_publish = typer.confirm("Initalize publish script?")
        if not package_name:
            print("Incomplete input, PACKAGE_NAME missing")
            exit(-1)
        os.mkdir(package_name)
        os.chdir(package_name)
        os.mkdir("src")
        os.chdir("src")
        with open("main.🔥", "w") as f:
            f.write("fn main() raises:\n\tprint('Hello from Mojo🔥!')")
            
        if make_repo:
            sb.run(["git", "init"])
        else:
            sb.run(["git", "remote", "add", "origin", repo_name])
            branch = input("Branch:")
            sb.run(["git", "branch", "-M", branch])
        with open("package.toml", "w") as f:
            version = input("Package version: ")
            f.write(f"[info]\nname={package_name}version={version}\n\n[Creator]\nname={CONFIG['usname']}")
            
        with open("README.md", "w") as f:
            f.write(f"# {package_name}\n\n### v{version}\nWrite your project documentation here!")
            
        ...
    
@app.command()
def delete(
        force:bool=typer.Option(help="Forcefully delete pkm, no questions asked 😉", default=False), 
        silent:bool=typer.Option(help="Silence the logs, only recieve error messages 🤫", default=False)
    ):
    """Uninstall pkm"""
    CONFIG["en-logs"] = False if not silent else True
    
        
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