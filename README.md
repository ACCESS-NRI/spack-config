# Spack Config

This repository contains:

* Spack configuration files required by the Spack instance(s) maintained by ACCESS-NRI on Gadi and ACCESS-NRI's [CI Docker image](https://github.com/ACCESS-NRI/build-ci/).
  * The deprecated `common-v0.2x` directory contains the required configuration files for older Spack 0.2x versions and should not be used directly.
  * For clarity, from Spack v1.1 onwards, we have removed symlinks in the versioned directory (e.g. `v1.1`) by storing the entire file.
  * Read the `v1.1/include/defaults.yaml` file to understand how the directories are used.

## Usage

* A regular user on Gadi does not need to clone this repository.

* An administrative user on Gadi simply needs to clone this repository as a sibling of the ACCESS-NRI/spack clone.

## References

* [Spack Configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes)
* [Spack Settings (config.yaml)](https://spack.readthedocs.io/en/latest/config_yaml.html)
* [Include Settings (include.yaml)](https://spack.readthedocs.io/en/latest/include_yaml.html)
* [Spack extended YAML Format](https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format)
