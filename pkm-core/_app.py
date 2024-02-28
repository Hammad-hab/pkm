from _registry import PackagesRepo, Registry, readPKMSourceFile
from _utils import abort, info, success, CONFIG
from _http import PKMGitClone
import os

"""
    FIXME: Security issues that might allow unauthorised access to repository
"""

class PKMManager:
    
    @staticmethod
    def hasInstalledPackage(package:str):
        installed_reg = readPKMSourceFile(Registry.INSTALLED_FILE)
        return installed_reg.hasPackage(package)
    
    def __init__(self) -> None:
        self.packages_repository = PackagesRepo()
        self.registry = self.packages_repository.getRegistry()
        self.installed_reg = readPKMSourceFile(Registry.INSTALLED_FILE)
        info(f"Loading Packages Registry (Local:{self.packages_repository.islocal})")
        pass
    
    def fetchPackage(self, package:str):
        if not self.registry.hasPackage(package):
            abort(f"Package {package} not in registry. Please check package name for any typos or try refreshing the local registry with pkm update", "Fetching Package")
        try:
            url = self.registry.getPackage(package)
            installer = PKMGitClone(url, package)
            installer.pkg_bin = CONFIG["pack-package"]
            installer.clone()
            self.installed_reg.addPackage(package, "0.0.1i")
            self.installed_reg.write_to(Registry.INSTALLED_FILE)
        except Exception as e:
            info(f"Failed to install {package}")
            abort(f"{e!r}", "Installing Package")
            raise
        success(f"Successfully installed {package}")