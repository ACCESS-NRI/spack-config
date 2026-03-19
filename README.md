# Spack Config

This repository contains:

* Spack configuration files required by the Spack instance(s) maintained by ACCESS-NRI on Gadi and ACCESS-NRI's [CI Docker image](https://github.com/ACCESS-NRI/build-ci/).
  * The `ci` directory is to be used by the CI Docker image.
  * The `gadi` directory is to be used in Gadi deployments.
  * The `common` directory is a subset of required configuration files for older Spack versions and should not be used directly.
  * The `common-api-v2` directory is a subset of required configuration files for Spack v1.1+ and should not be used directly.

* `spack-enable.bash` is for general users to set their `bash` environment to directly run `spack` commands using ACCESS-NRI's Spack instance(s). Execute: `. spack-enable.bash`. It disables local configuration changes in `~/.spack`.

## Usage

`ln -s -r -v <SPACK_VERSION>/<SPACK_SITE>/* <SPACK_ROOT>/etc/spack/site/`

Where,
* <SPACK_VERSION> is the spack major version. e.g. `v0.20`.
* <SPACK_SITE> is `ci` or `gadi`.
* <SPACK_ROOT> is the root directory of the Spack instance.

## References

* [Spack Configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes)
* [Spack Settings (config.yaml)](https://spack.readthedocs.io/en/latest/config_yaml.html)
* [Spack extended YAML Format](https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format)
