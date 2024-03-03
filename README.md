<div align="center">
  <h1>PKM</h1>
  <h4>Mojo's unofficial community package manager</h4>
  <p align="center">
</div>
Mojo is a new programming language and while it has many features in its recent versions, it lacks a package manager. So until Mojo has its own package manager by Modular, `pkm` is there to temporarily fill that space.

## Quick Start

`pkm` has been designed to be simple and extremely user friendly so its commands are mostly self-explanatory. Following are their uses and descriptions

### Installation

1) Run the command `curl -L https://raw.githubusercontent.com/Hammad-hab/pkm/main/install.py >> install.py`
2) This will create a file named `install.py` in the current directory
3) After the file has been installed, run `install.py`. The script will automatically install pkm into your system

To check if `pkm` has been installed correctly, run `pkm info`. If you encounter an error, please report it at `issues` tab.

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
* `--force`: Forcefully delete a package without any confirmation prompts.

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

Used to create a repository account/package

**Syntax**:
          `pkm create <account || package>`

> `pkm create account`
Create an account. It prompts you for the username and password for your registration.
**Options**:

* `--autologin` (**default=`False`**): Automatically login as soon as you create the account

> `pkm create package`

Initialize an empty package with ease. When this command runs it prompts you for the package name, version et cetera.
It will create a `./src` directory, a `README.md `, `package.toml `and a `main.🔥` file.

> #### `pkm delete`

Delete `pkm` from your system

**Options**:

`--force`: Forcefully delete a `pkm` without any confirmation prompts.

`--silent`: Disable all kind of logs (error's are still shown).

> #### `pkm info`

Get info regarding your `pkm` copy, usually it's location, version etc.

### Upload a package

To upload a package you can use `pkm upload` command built into `pkm`. Following are the steps you should generally follow in order to upload a package:
1) Upload your package to github in any way you choose
2) Run `pkm upload`
3) The cli will prompt you for your login details and package information
4) Type in your username and password if you have an account. If you do not have an account, you can create one by running `pkm create account` (See above for usage)
5) Insert the package name and repository
6) Press [`ENTER`] to upload the package to the repository