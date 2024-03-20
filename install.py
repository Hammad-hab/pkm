from git import Repo, RemoteProgress
import os, sys
import shutil
import uuid
import subprocess
from base64 import b64decode

print("Installing dependencies for python2 and lower (pip)")
os.system("python3 -m pip install GitPython termcolor firebase-admin rich typer validators tomli")
print("Installing dependencies for python3 (pip3)")
os.system("python3 -m pip3 install GitPython termcolor firebase-admin rich typer validators tomli")
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
        
certificate = ("ew0KICAgICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsDQogICAgInByb2plY3RfaWQiOiAi"
"cGttLW1hbmFnZXIiLA0KICAgICJwcml2YXRlX2tleV9pZCI6ICI4Yzk0ZjRmNThiN2ZjZGYzMjU4YzE2OTA"
"wNDhjMzZiMjVhYzdlNTdlIiwNCiAgICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFW"
"S0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUURmT2tUc1BkVVAva2Z"
"nXG5sbGlYR2Rqdjd6RzhhbmZPamNYV1N4N0dwa3E0cWVQakt0b1praWNzOEMrT1lBRGwxZVgyeEh4SEdpMkhoM0xSXG4rU"
"FhQUlRWT0lCT3VQc2ZCbkd0L1JIQlpuUmdrUVMrb3JyQ2FpMjBvT3BXa2YyYSs0OTBWOGtjMGdFTlNNQXoyXG5xWWZVRXdBe"
"mt4Smd0YmZyUzc1ODVqdnF1dnYyZk9PTnFIellXSFgzN2pPUnV0NGZESG8rNzJxM3VIbW54WU41XG50ZDB5QmtTY2dqTVMrdi"
"9oWXNsMWFwdmlDZ2J6MmxXMno2WWR0WnA5MEFPdUNXVjhZSlJsZEZxSmI5L0VvVHZVXG5PcUhZeDhxc2VKalVaREFWZ3NmZVZE"
"RzgzUkJvV20yYytoeWZkZmFIdkNYSlVhc0plM3lqTUZPc3g5djBxaSt0XG5yRzR5VDJMZEFnTUJBQUVDZ2dFQUZVZlpDN3QrVF"
"JyRTcrcHRVaVJXNjlLK0IxUVFEVnN6SmRGK0F0cVdDNEk0XG50UzZmNGFtdS9lZjg1S0lPMjlwWEpMNEpDZjg3SVcwK2V6bDBk"
"NWpGc3VlNGNKZFFGRXRNN1RKUlVwMjVFRFc5XG5yU05RTno5OC9jV09BQU5jUUd6NUplODFyaEhmT1IzWEVvbkpadVNUMDViYy"
"9PYTkvSnE1TTIrQWZVbHJuVTBQXG5qUVBQRGhGWS84cSt1QVZqZmE2Q0F3bXhFa0xSbmZwcWViR3NwV2pEQjU1eWVJU3h0V0VL"
"azRlZnZxaUVsRWM5XG5aRFkzWWd2RWFIM01VSkxiaXlUNDA2ZzhXRUxSeGs1dkZMUnJyeDQ1ZEIxaHptWW56dUZvZlNnQUNBZU"
"5QZ0JIXG51UUpBVWpuNHEwUlJ6Wkl2aWZnZVcyc2R1YnlzZW1rZWxSRlZqNHF3Z1FLQmdRRDFmcWFWNXNnV0cvQXYzMHdaXG43b"
"jF4VkRvVlgwNnRmSWd3MHdzTGx0WVhuQXc5KzF2UHdJMUV6L0pOUVZuS3paM1FBM2NzUGg1bkdhTzYyNFVZXG5HdVFaSXEweXp1SFpSYTRx"
"RUdORGRaNk84K1h3SU5uNjNTdk1jNWxtSXJUK0lvVWV4VE5HUmpxZ0N0Unoxamp4XG5OakJqbkJ1ZHAvenJUMWR0UE8vNysvMjRYUUtCZ1FE"
"b3g2KzIwdVg2YTY1QnM0NFo3OHhWMnZTWUMwQ0gzTENKXG5GM3d2a1hDaHJxcDJmZkJ6dm14R3ZhaEcvcXg1M1oyM3VQUnBib2orb0"
"M2clA3cGFlTjg0dVFuc2FGenFhYXpRXG5BK3o4eUs0RTd5Q1VDZDF3aWpBdk1qU1laeXVZSlRkbkVVNXJZb2dFSVErRkM3WnU1WTBuKzErYllZ"
"TXgxVXBjXG5LT1ByaUlPc2dRS0JnRmNEYmc1QnYzZStyVko2aGlIRzIyV1k0Z0dEUjRMTVdnVmNPRlVDUUo0YnJHY251YklZXG5ZTG9jTHBqZGFmTXR"
"FQnVUcnVEYW43SVJiMndpdExrSGh3TzF1OGYvZGlPcHhBS2F6bVF4dzJLTjVsbEhlNXVrXG5Xd3JiaW1xZU1LTEhINEg1aWFRRjdtK2RoeElMd3lFVUF"
"QQzllemhWTzVzNEF4ZnYrbXZKTkhQdEFvR0FIRys0XG5jWGNXRFI5MmJDUkpLYlgzbWsxakwrZS8vRmpqWC92MGVjTWtwVHUzS3o"
"1N1QwaGw1Y1pwZGpMS1V5RFZrWW9RXG5vWWlWUjdXOXZjSE5QQndqK01QeUNHVS9aSXVBUnZFVDFGV1huSmF4dmlQdVh6OGlYOEd"
"jVnpuVFE0VFlYY2pwXG5jWWpaNE5kQkZCbTRNWmZ0UklNYXpOcCtzbW5CNmJ3OUM1cmpxd0VDZ1lFQTZwRVVOTCsyeUw0a2ZHRjlx"
"RHR5XG52V3BrdHF4TGFxMnorME9VZkt4Y3ZFb0FSYkh6anFiSytCbU1za3h1UmllZXovTUxuT05nbUxZSDZiMEg4RGRWXG5OQ09G"
"cmZBSVh1MUxIbmZiYXdWb2g4RTRXNk50cXQwMFFNM1h6bFlURkRnS1loNGNhRHVrUmliMDFOV2ZrZVpzXG42cTBaUlNRQXhhUHFq"
"ZHZydFdsd3I2UT1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsDQogICAgImNsaWVudF9lbWFpbCI6ICJmaXJlYmFzZS1h"
"ZG1pbnNkay1neHpudEBwa20tbWFuYWdlci5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsDQogICAgImNsaWVudF9pZCI6ICIxMDU2N"
"jg5OTc5OTYyNTY0MDY3OTEiLA0KICAgICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0"
"aCIsDQogICAgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsDQogICAgImF1dGhfcHJvdmlkZ"
"XJfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMiLA0KICAgICJjbGllbnRfeD"
"UwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L2ZpcmViYXNlLWFkbW"
"luc2RrLWd4em50JTQwcGttLW1hbmFnZXIuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLA0KICAgICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ"
"2xlYXBpcy5jb20iDQp9")
if 'SUDO_USER' in os.environ:
    username = os.environ['SUDO_USER']
else:
    username = os.getenv('USER') or os.getenv('USERNAME')


clone_repository = "https://github.com/Hammad-hab/pkm.git"
tool_name = f"pkm@{uuid.uuid4()}"
target_path = f"/usr/local/bin/{tool_name}"
repository = Repo.clone_from(clone_repository, target_path, progress=GenericProgress())
print("\nSuccessfully cloned repo. Setting up pkm...")
os.remove(target_path + "/LICENSE")
shutil.move(f"{target_path}/pkm-core", "/usr/local/bin/")
shutil.rmtree(target_path)
os.rename(f"/usr/local/bin/pkm-core", f"/usr/local/bin/pkmd")
with open(f"/usr/local/bin/pkmd/__main__.py", "r") as f:
    contents = f.read().replace("INSTALLER<INSERT_PYTHON_PATH>", "!" + subprocess.run(["which", "python3"], capture_output=True).stdout.decode("utf-8"))
    f.close()
    
with open(f"/usr/local/bin/pkmd/__main__.py", "w") as f:
    f.write(contents)
    f.close()

SHELL_PROP_SRC = \
"""
#!/bin/zsh
python3 /usr/local/bin/pkmd/__main__.py $@
"""

with open(f"/usr/local/bin/pkm", "w") as f:
    print("Writing shellscript bindings")
    f.write(SHELL_PROP_SRC)
    f.close()

with open(f"/usr/local/bin/pkmd/certificate.json", "w") as f:
    print("Creating Repository certificate")
    f.write(b64decode(certificate).decode("utf-8"))
    f.close()

print("Running privilege commands")
subprocess.run(["chmod", "+x", "/usr/local/bin/pkm"])
print("Successfully downloaded pkm")