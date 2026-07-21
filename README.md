# ACCESS-NRI Spack Config

This repository contains:

* Spack configuration files required by the Spack instance(s) maintained by ACCESS-NRI on Gadi and ACCESS-NRI's [CI Docker image](https://github.com/ACCESS-NRI/build-ci/).
  * The deprecated `common-v0.2x` directory contains the required configuration files for older Spack 0.2x versions and should not be used directly.
  * For clarity, from Spack v1.1 onwards, we have removed symlinks in the versioned directory (e.g. `v1.1`) by storing the entire file.
  * Read the `v1.1/include/user/include.yaml` file to understand the configuration and directory hierarchy. File `v1.1/include/admin/include.yaml` describes the configuration used by the Pre-release and Release Spack instances.

## Usage

### Gadi Regular user

* A regular user on Gadi does not need to clone this repository. Simply follow the instructions in [How to use Spack on Gadi for building ACCESS models](https://docs.access-hive.org.au/getting_started/spack/).

* The default `install_tree` is `/g/data/$PROJECT/$USER/spack/1.1/release`.

### Gadi Advanced user (Optional)

The shared Spack instance contains a read-only `access-spack-packages` repository. If there is a need to modify a Spack Package Recipe (SPR) or choose an older version of the repository, simply add an _editable_ Spack repository by using `spack repo add`. Run `spack repo list` to see all the enabled repositories in order of highest precedence to lowest precedence.

#### Create an editable access-spack-packages _in_ a Spack environment

This option will isolate the new editable `access-spack-packages` repository by only adding it to a single Spack environment, after cloning the repository inside the same directory as the `spack.yaml` file. Other Spack environments will be completely unaffected. The following commands must be run _after_ activating a Spack environment:
```
spack cd -e
git clone https://github.com/ACCESS-NRI/access-spack-packages
spack repo add access-spack-packages/spack_repo/access/nri
```

#### Create an editable access-spack-packages _outside_ a Spack environment

By running the following commands, Spack will choose to use the editable `access-spack-packages` repository with all Spack environments and when an environment is not activated:
```
cd /g/data/$PROJECT/$USER/spack/1.1
git clone https://github.com/ACCESS-NRI/access-spack-packages
spack repo add --scope=access.nri.gadi.user access-spack-packages/spack_repo/access/nri
```

#### Choose an older version of access-spack-packages repository

Immediately after creating an _editable_ `access-spack-packages` repository, and before changing the current directory, run:
```
git -C access-spack-packages switch -c <spack_packages_version> <spack_packages_version>
```

#### Update Spack repositories

Run `spack repo list` to identify the name of the repository.

```
cd $(spack location --repo <name-of-repository>)
git fetch origin
git reset --hard origin/<current-branch-name>
```

#### Ignore pre-built upstream Spack packages

Spack will use a pre-built upstream package rather than rebuild it. If there is a need to force the rebuilding of the source package, upstreams can be disabled by running:

1. `mkdir -p /g/data/tm70/hj1810/spack/1.1/spack-user-config`
2. `spack config --scope=access.nri.gadi.user edit upstreams` and insert `upstreams:: {}`

To re-enable upstreams, run: `spack config --scope=access.nri.gadi.user edit upstreams` and delete `upstreams:: {}`.

### Gadi Admin user

#### Install Release Spack instance

```
git clone https://github.com/ACCESS-NRI/spack.git --branch access/releases/v1.1-admin
git clone https://github.com/ACCESS-NRI/spack-config.git
. spack/share/spack/setup-env.sh
export SPACK_USER_CACHE_PATH="$SPACK_ROOT/../spack-admin-cache"
spack bootstrap now
```

#### Install Shared Spack instance

```
git clone https://github.com/ACCESS-NRI/spack.git --branch access/releases/v1.1
git clone https://github.com/ACCESS-NRI/spack-config.git
. spack/share/spack/setup-env.sh
export SPACK_USER_CACHE_PATH="/g/data/$PROJECT/$USER/spack/$SPACK_VERSION/spack-user-cache"
spack repo update
```

Do _not_ run `spack bootstrap now` as the service user because it create temporary and permanent files in `/g/data/$PROJECT/$USER/spack/$SPACK_VERSION`.

#### Update Spack instance
```
git -C spack fetch --all -Pp
git -C spack reset --hard origin/access/releases/v1.1
git -C spack-config pull
. spack/share/spack/setup-env.sh
spack repo update
```


## Spack Architecture for CI and Gadi with Spack v1.1 (2026)

### Objective

* A user on Gadi shall NOT need to run `git clone` to use Spack.
* The CI Spack architecture/configuration shall be based on the Gadi architecture/configuration to ensure additional testing coverage.

### Users

* Gadi service user
  * Responsible for Pre-release and Release
* Gadi regular user
  * Modify and build Model Deployment Repository
* Gadi advanced user
  * Modify Spack Package Recipes

* Build-ci
  * Upstream Docker image
  * Runner Docker image

### Solution

* Using Spack v1.1's include.yaml mechanism allows defining tiered configuration directories with a common directory for both Gadi and CI.

* Using Spack v1.1's include.yaml mechanism choose a `spack-config` directory based on the `hostname` of the system.

* Define an `upstream` for the Gadi user and CI runner to speed up builds.
```
╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ Upstream / Admin User     ┊
┊ ---------------------     ┊
┊                           ┊
┊ $spack/..                 ┊
┊ ├── access-spack-packages ┊
┊ ├── bootstrap             ┊
┊ ├── cache                 ┊
┊ ├── environments          ┊
┊ ├── intel                 ┊
┊ ├── release               ┊
┊ ├── release/modules       ┊
┊ ├── sourcecache           ┊
┊ ├── spack                 ┊
┊ ├── spack-admin-cache     ┊
┊ ├── spack-admin-config    ┊
┊ ├── spack-config          ┊
┊ └── spack-packages        ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯
              |
              V
╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ Downstream / Regular User        ┊
┊ -------------------------        ┊
┊                                  ┊
┊ /g/data/$PROJECT/$USER/spack/1.1 ┊
┊ ├── bootstrap                    ┊
┊ ├── cache                        ┊
┊ ├── environments                 ┊
┊ ├── release                      ┊
┊ ├── release/modules              ┊
┊ ├── sourcecache                  ┊
┊ ├── spack-user-cache             ┊
┊ └── spack-user-config            ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯
```

* Use Spack scopes to differentiate between the configuration of an `upstream`  and a `downstream`. Scopes in highest to lowest precedence order:

#### v1.1/include/user/include.yaml

```
- name: "access.nri.gadi.user"
  path: "/g/data/$PROJECT/$USER/spack/1.1/spack-user-config"
  optional: true
  when: '"gadi.nci.org.au" in hostname'

╭╌╌╌╌╌╌╌╮
┊ empty ┊
╰╌╌╌╌╌╌╌╯

- name: "access.nri.ci.user"
  path: "$spack/../runner/spack-user-config"
  optional: true
  when: '"gadi.nci.org.au" not in hostname'

╭╌╌╌╌╌╌╌╮
┊ empty ┊
╰╌╌╌╌╌╌╌╯

- name: "access.nri.gadi.downstream"
  path: "$spack/../spack-config/v1.1/gadi/downstream"
  when: '"gadi.nci.org.au" in hostname'

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1/gadi/downstream ┊
┊ ├── bootstrap.yaml   ┊
┊ ├── config.yaml      ┊
┊ ├── modules.yaml     ┊
┊ └── upstreams.yaml   ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯

- name: "access.nri.ci.downstream"
  path: "$spack/../spack-config/v1.1/ci/downstream"
  when: '"gadi.nci.org.au" not in hostname'

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1/ci/downstream ┊
┊ ├── bootstrap.yaml ┊
┊ ├── config.yaml    ┊
┊ ├── modules.yaml   ┊
┊ └── upstreams.yaml ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯

- name: "access.nri.gadi"
  path: "$spack/../spack-config/v1.1/gadi"
  when: '"gadi.nci.org.au" in hostname'

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1/gadi         ┊
┊ ├── modules.yaml  ┊
┊ └── packages.yaml ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯

- name: "access.nri.defaults"
  path: "$spack/../spack-config/v1.1"

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1                 ┊
┊ ├── bootstrap.yaml   ┊
┊ ├── concretizer.yaml ┊
┊ ├── config.yaml      ┊
┊ ├── modules.yaml     ┊
┊ ├── packages.yaml    ┊
┊ ├── repos.yaml       ┊
┊ ├── toolchains.yaml  ┊
┊ └── upstreams.yaml   ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯
```

#### v1.1/include/admin/include.yaml

```
- name: "access.nri.admin"
  path: "$spack/../spack-admin-config"
  optional: true

╭╌╌╌╌╌╌╌╮
┊ empty ┊
╰╌╌╌╌╌╌╌╯

- name: "access.nri.gadi"
  path: "$spack/../spack-config/v1.1/gadi"
  when: '"gadi.nci.org.au" in hostname'

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1/gadi         ┊
┊ ├── modules.yaml  ┊
┊ └── packages.yaml ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯

- name: "access.nri.defaults"
  path: "$spack/../spack-config/v1.1"

╭╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╮
┊ v1.1                 ┊
┊ ├── bootstrap.yaml   ┊
┊ ├── concretizer.yaml ┊
┊ ├── config.yaml      ┊
┊ ├── modules.yaml     ┊
┊ ├── packages.yaml    ┊
┊ ├── repos.yaml       ┊
┊ ├── toolchains.yaml  ┊
┊ └── upstreams.yaml   ┊
╰╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╯
```


## References

* [Spack Configuration Scopes](https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes)
* [Spack Settings (config.yaml)](https://spack.readthedocs.io/en/latest/config_yaml.html)
* [Include Settings (include.yaml)](https://spack.readthedocs.io/en/latest/include_yaml.html)
* [Spack extended YAML Format](https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format)
