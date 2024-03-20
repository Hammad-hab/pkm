<div align="center">
  <h1>PKM Changelog</h1>
  <img src="docs/icon.png" width="100px"/>
  <h4>List of all the changes made from <code>v1.0</code> onwards</h4>
  <p align="center">
</div>

# v1.0.0 Stable

* Better documentation
* Added commands: `pkm create account` and `pkm create package`
* Added Auto package creation feature (i.e template)
* Added Extensions and hooks for customizing pkm
* Added a more secure way to distribute certificate
* Added account creation capability

## v1.0.1 Stable

* Installation Bug fix (`Typer` module missing)
* Added command `pkm listpkgs`
* Added a crude GUI option in `listpkgs`
* Added `CHANGELOG` for `v1.0.0` and onwards
* Updated documentation
* Tkinter bug fix (`Module not found`)
* Changed architecture to contain more complex information and to support scalability
  * Initially pkm used a `one-line` information storage strategy that had it's limitations:
    ``<package_name>=<repository_url>``
    This was hard to comprehend and scale so it was replaced by a more Object based storage:
    ```xml
    <pkg_name>: <name>
    <pkg_repo>: <repo>
    <pkg_creator>: <creator>
    ...
    ```
* Packages that have been created using `pkm create package` are now easier to upload. Since `pkm` stored
  all their metadata upon creation, it will automatically fetch it and upload the package.
