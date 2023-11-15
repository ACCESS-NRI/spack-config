# Spack Config

Shared spack configuration for building software on gadi@NCI

## Steps to create configuration

Initial steps were to use in-built `spack` tools to find external system tools and compilers:
```bash
spack external find
```

That picks up a bunch of system tools we're probably pretty agnostic about as far as versions go. Mostly just need builds to be reproducible, so the less we have to install as dependencies the better. But only finds tools in `/usr`, not additional versions that are module-loadable.

```bash
spack compiler find
Picked up some of the available compilers, but not all, and doesn't necessarily determine the required environment modules properly. 
```

It is possible to `module load` compilers or external packages and then run `spack compiler find`, but this also tends to auto-detect a lot of the variants which can also cause incompatibilities. As we definitely don't want to build some important dependencies, such as openmpi and compilers, or less important "tools" like perl and python, then the detail of the variants just complicates the `spec` and creates the possibilities of incompatibilities later if/when variants are removed. 

Consequenrly added an un-buildable virtual mpi package to `~/.spack/packages.yaml` which forces any MPI dependency to use one fo the installed MPI libraries.
```yaml
packages:
  # Add a virtual mpi package and set it to not be buildable, to force using available external MPI
  mpi:
    buildable: false
```

Also added `buildable: false` to a number of the other external tools to prevent unnecessary building of extraneous build tools.

Running
```python
python -mpdb find_compilers_packages.py -v
```
will update `compilers.yaml` and `packages.yaml` in-place in the current directory. It will respect all existing packages, but update the packages specified in the script.