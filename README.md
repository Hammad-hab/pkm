
# pkm,

### Mojo's unofficial community package manager

Mojo is a new programming language and while it has many features in it's recent versions, it lacks a package manager. So until Mojo has it's own package manager by Modular, `pkm` is there to temporarily fill that space.

### Quick Start

`pkm` has been designed to be simple and extremely user friendly so it's commands are mostly self-explanatory. Following are their uses and descriptions

>  #### `pkm install`

Used for installing a package.
**Syntax**:
          `pkm install <package_name> [--disable-logs| --no-disable-logs | --pack | --no-log]`
**Attributes**:

* `--disable-logs`: Silence the `pkm` installer logs. This means that no success or info logs will be shown, only errors
  * `--no-disable-logs`(**default**): This is the *default* value of the en-logs configuration i.e logs are **not** disabled
* `--pack` (**default**): Mojo has an amazing ability to compile it's packages into a
  .📦 (`.mojopkg`). The `--pack` ensures that the installed package is compiled into a .📦.
  * `--no-pack`: Like it's name suggests, it prevents `pkm` from
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


> #### `pkm update`