import shutil
import git
import os
from _utils import info, warn, success, Progress

class PKMGitClone:
    __TMP_FOLDER_NAME = "tmp" # name of the temporary folder
    __MND_DIR = "mojo_modules/" # name of the mojo_modules folder
    
    
    def __init__(self, url:str, pkgname:str) -> None:
        self.git_repo_url = url
        self.pkgname = pkgname
        info("Created PKMGitClone instance")

    def clone(self):
        info("Executing Pre-clone operations")
        if not os.getcwd().endswith(PKMGitClone.__MND_DIR):
            warn("User is not in mojo_modules, changing directory")
            os.chdir(os.getcwd() + "/" + PKMGitClone.__MND_DIR)
        tmp_relative = os.getcwd() + "/" +PKMGitClone.__TMP_FOLDER_NAME
        try:
            info(f"Cloning repositiory {self.git_repo_url} of package {self.pkgname}")
            repositiory = git.Repo.clone_from(self.git_repo_url, tmp_relative, progress=Progress()) # type: ignore
            print()
            success(f"Successfully cloned repository {self.git_repo_url}")
            os.chdir(tmp_relative)
            info("Deleting tmp/ files and setting up project")
            shutil.move(tmp_relative + "/" + self.pkgname, "../")
            shutil.rmtree(tmp_relative)
            success(f"Successfully deleted tmp files")
            
            return repositiory
        except:
            info("Performing Cleanup due to error")
            shutil.rmtree(tmp_relative)
            raise
            
    def refresh(self, url:str, pkgname:str):
        self.git_repo_url = url
        self.pkgname = pkgname
