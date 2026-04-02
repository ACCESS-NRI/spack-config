# Spack Config

This repository contains:

* Spack configuration files required by the Spack instance(s) maintained by ACCESS-NRI on Gadi and ACCESS-NRI's [CI Docker image](https://github.com/ACCESS-NRI/build-ci/).
  * The `common` directory contains the required configuration files for older Spack versions and should not be used directly.
  * The `common-api-v2` directory contains the required configuration files for Spack v1.1+ and should not be used directly.
  * Read the `v1.1/include/defaults.yaml` file to understand how the directories are used.

## Usage

Simply clone this repository as a sibling of the ACCESS-NRI/spack clone.

## References

* [Spack Configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes)
* [Spack Settings (config.yaml)](https://spack.readthedocs.io/en/latest/config_yaml.html)
* [Include Settings (include.yaml)](https://spack.readthedocs.io/en/latest/include_yaml.html)
* [Spack extended YAML Format](https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format)
