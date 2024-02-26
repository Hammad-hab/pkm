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
os.remove(target_path + "/LICENSE")
shutil.move(f"{target_path}/src", "/usr/local/bin/")
shutil.rmtree(target_path)
os.rename(f"/usr/local/bin/src", f"/usr/local/bin/pkmd")
with open(f"/usr/local/bin/pkmd/__main__.py", "r") as f:
    contents = f.read().replace("INSTALLER<INSERT_PYTHON_PATH>", "!" + subprocess.run(["which", "python3"], capture_output=True).stdout.decode("utf-8"))
    f.close()
    
with open(f"/usr/local/bin/pkmd/__main__.py", "w") as f:
    f.write(contents)
    f.close()

SHELL_PROP_SRC = \
"""
# prop >> __main__.py
echo Welcome to PKM
python3.10 /usr/local/bin/pkmd/__main__.py $@
"""

with open(f"/usr/local/bin/pkm.sh", "w") as f:
    f.write(SHELL_PROP_SRC)
    f.close()