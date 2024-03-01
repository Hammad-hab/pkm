<div align="center">
  <h1>PKM</h1>
  <h4>Mojo's unofficial community package manager</h4>
  <p align="center">

Mojo is a new programming language and while it has many features in its recent versions, it lacks a package manager. So until Mojo has its own package manager by Modular, `pkm` is there to temporarily fill that space.

## Quick Start

`pkm` has been designed to be simple and extremely user friendly so its commands are mostly self-explanatory. Following are their uses and descriptions

### Installation

* Run the command `curl -L https://raw.githubusercontent.com/Hammad-hab/pkm/main/install.py >> install.py`
* This will create a file named `install.py` in your directory
* After the file has been installed, run `install.py`. The script will automatically install pkm into your system

> #### `pkm install`

Used for installing a package.

**Syntax**:
          `pkm install <package_name> [--disable-logs| --no-disable-logs | --pack | --no-log]`
**Attributes**:

* `--disable-logs`: Silence the `pkm` installer logs. This means that no success or info logs will be shown, only errors
  * `--no-disable-logs`(**default**): This is the *default* value of the en-logs configuration i.e logs are **not** disabled
* `--pack` (**default**): Mojo has an amazing ability to compile its packages into a
  .📦 (`.mojopkg`). The `--pack` ensures that the installed package is compiled into a .📦
  * `--no-pack`: Like its name suggests, it prevents `pkm` from
    using `mojo package` to compile the package into a .📦

> #### `pkm purge`

Used for purging (removing/uninstalling) a package.

**Syntax**:
        `pkm purge <package_name> [--disable-logs| --no-disable-logs]`
**Attributes**:

* `--disable-logs`: Silence the `pkm` installer logs. This means that no success or info logs will be shown, only errors
  * `--no-disable-logs`(**default**): This is the *default* value of the en-logs configuration i.e logs are **not** disabled

> #### `pkm has`

Used to check if a `pkm` package has been installed

**Syntax**:
        `pkm has <package_name>`

> #### `pkm config`

Used to print the default configuration of `pkm`
(**deprecated**)

> #### `pkm update`

Updates the local package list

**Syntax**:
          `pkm update`

**Detailed Explanation**
`pkm` downloads packages from different places so in order to ensure minimal server interaction, `pkm` like `apt`/`apt-get` maintains a `sources.list` which contains all the packages and their locations.
If the original repository has a new package, `pkm` won't know until the `sources.list` is updated.

> #### `pkm upload`

Upload a package to the `pkm` repository

**Syntax**:
         `pkm upload [--record_creds| --no-record-creds | --ignore-stored | --no-ignore-stored]`
**Attributes**:

* `--record-creds` (`True`/`False`): specify if you want to prevent pkm from storing your credentials to prevent you from  having to login every time you upload a package
* `--ignore-stored` (`True`/`False`): specify if forcefully want pkm to ignore record credentials. This is useful if you want
  to login again.

> #### `pkm create`

Used to create a repository account

**Syntax**:
          `pkm create`
