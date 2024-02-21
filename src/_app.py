from _registry import PackagesRepo, Registry
from _utils import abort, info, success
from _http import PKMGitClone
import os


class PKMManager:
    def __init__(self) -> None:
        self.packages_repository = PackagesRepo()
        self.registry = self.packages_repository.getRegistry()
        info(f"Loading Packages Registr (Local:{self.packages_repository.islocal})")
        pass
    
    def fetchPackage(self, package:str):
        if not self.registry.hasPackage(package):
            abort(f"Package {package} not in registry. Please check package name for any typos or try refreshing the local registry with pkm update", "Fetching Package")
        try:
            url = self.registry.getPackage(package)
            installer = PKMGitClone(url, package)
            installer.clone()
        except Exception as e:
            info(f"Failed to install {package}")
            abort(f"{e!r}", "Installing Package")
        success(f"Successfully installed {package}")
        
manager = PKMManager()
manager.fetchPackage("stdlib_extensions")