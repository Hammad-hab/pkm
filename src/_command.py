import typer, os
from _utils import CONFIG, warn, console, abort, color, success
from _app import PKMManager, readPKMSourceFile, Registry
from _http import PKMGitClone
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
def purge(package_name: str, disable_logs:bool=False):
    CONFIG["en-logs"] = not disable_logs
    if PKMManager.hasInstalledPackage(package_name):
        delpackage = typer.confirm(color(f"Are you sure you want to delete {package_name}?", color="yellow"))
        if not delpackage:
            raise typer.Abort()
        warn(f"Deleting {package_name}...")
        os.remove(PKMGitClone._MND_DIR + package_name + ".mojopkg")
        success(f"Successfully deleted package {package_name}")
        installed_reg = readPKMSourceFile(Registry.INSTALLED_FILE)
        installed_reg.removePackage(package_name)
        installed_reg.write_to(Registry.INSTALLED_FILE)
        success(f"Successfully updated package registry {Registry.INSTALLED_FILE}")
        
    else:
        abort("User tried to purge a package that hasn't been instaled", "Purging a package")
        


@app.command()
def has(package_name: str):
    "Check if a package has been installed"
    console.print(PKMManager.hasInstalledPackage(package_name))
    
@app.command()
def config():
    "Print the default Configuration"
    console.print_json(data=CONFIG)

if __name__ == "__main__":
    app()