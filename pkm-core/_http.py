import shutil
import git
import os
from _utils import info, warn, success, Progress,errmsg, CONFIG


class PKMGitClone:
    _TMP_FOLDER_NAME = "tmp" # name of the temporary folder
    _MND_DIR = f"/Users/{CONFIG['usname']}/.modular/pkg/packages.modular.com_mojo/lib/mojo/" # name of the mojo_modules folder
    PACK = False
    
    def __init__(self, url:str, pkgname:str) -> None:
        self.git_repo_url = url
        self.pkgname = pkgname
        self.pkg_bin = PKMGitClone.PACK
        info("Created PKMGitClone instance")
    def clone(self):
        info("Executing Pre-clone operations")
        if not os.getcwd() == (PKMGitClone._MND_DIR):
            warn("User is not in mojo_modules, changing directory")
        tmp_relative = PKMGitClone._MND_DIR + PKMGitClone._TMP_FOLDER_NAME
        try:
            info(f"Cloning repositiory {self.git_repo_url} of package {self.pkgname} into {tmp_relative}")
            repositiory = git.Repo.clone_from(self.git_repo_url, tmp_relative, progress=Progress()) # type: ignore
            print()
            success(f"Successfully cloned repository {self.git_repo_url}")
            info("Deleting tmp/ files and setting up project")
            shutil.move(tmp_relative + "/" + self.pkgname, PKMGitClone._MND_DIR + self.pkgname)
            shutil.rmtree(PKMGitClone._MND_DIR + PKMGitClone._TMP_FOLDER_NAME)
            if self.pkg_bin:
                os.system(f"mojo package {PKMGitClone._MND_DIR + self.pkgname} -o {PKMGitClone._MND_DIR + self.pkgname}.mojopkg")
                shutil.rmtree(PKMGitClone._MND_DIR + self.pkgname)
            success(f"Successfully deleted tmp files")
            
            return repositiory
        except:
            info("Performing Cleanup due to error")
            if os.path.isdir(PKMGitClone._MND_DIR + PKMGitClone._TMP_FOLDER_NAME):
                shutil.rmtree(PKMGitClone._MND_DIR + PKMGitClone._TMP_FOLDER_NAME)
            errmsg(f"Failure while cloning repo into {tmp_relative}")
            if os.path.isdir(PKMGitClone._MND_DIR+self.pkgname):
                errmsg(f"PKM could not install package {self.pkgname} because it is already installed")
            raise
                        
    def refresh(self, url:str, pkgname:str):
        self.git_repo_url = url
        self.pkgname = pkgname