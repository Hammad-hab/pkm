from git import Repo, RemoteProgress
import os, sys
import shutil
import uuid
import subprocess
class GenericProgress(RemoteProgress):
    def update(self, op_code: int, cur_count: str | float, max_count: str | float | None = None, message: str = "") -> None:
        if max_count is not None:
            completed = int(cur_count / max_count * 50)  # Using 50 characters for the progress bar #type:ignore
            remaining = 50 - completed
            progress_bar = "Installing pkm [%s%s]" % ('▓' * completed, '░' * remaining)
            sys.stdout.write("\r%s" % progress_bar)
            sys.stdout.flush()
        else:
            sys.stdout.write("\rInstalling pkm [%s]" % ('▓' * int(cur_count / 10))) #type:ignore
            sys.stdout.flush()
        sys.stdout.write(" %s" % message)
        sys.stdout.flush()

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
#!/bin/zsh
python3.10 /usr/local/bin/pkmd/__main__.py $@
"""

with open(f"/usr/local/bin/pkm", "w") as f:
    f.write(SHELL_PROP_SRC)
    f.close()
subprocess.run(["chmod", "+x", "/usr/local/bin/pkm"])