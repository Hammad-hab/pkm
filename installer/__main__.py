from git import Repo
import os
import shutil
import uuid
import subprocess
from installer_utils import GenericProgress

if 'SUDO_USER' in os.environ:
    username = os.environ['SUDO_USER']
else:
    username = os.getenv('USER') or os.getenv('USERNAME')

clone_repository = "https://github.com/Hammad-hab/pkm"
tool_name = f"pkm@{uuid.uuid4()}"
target_path = f"/usr/local/bin/{tool_name}"
installer_dir = f"/usr/local/bin/{tool_name}/installer"
repository = Repo.clone_from(clone_repository, target_path, progress=GenericProgress())
shutil.rmtree(installer_dir)
os.remove(target_path + "/.gitignore")
shutil.move(f"{target_path}/src", "/usr/local/bin/")
shutil.rmtree(target_path)
os.rename(f"{target_path}/src", f"{target_path}/pkm")
with open(f"{target_path}/pkm/__main__.py", "r") as f:
    contents = f.read().replace("#INSTALLER<INSERT_PYTHON_PATH>", subprocess.run(["which", "python3"], capture_output=True))
    f.close()
    
with open(f"{target_path}/pkm/__main__.py", "w") as f:
    f.write(contents)
    f.close()