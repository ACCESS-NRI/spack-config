# This is not an executable! Do not enable execute permissions.
# You need to be running a bash shell, then execute: . spack-start.bash

# Required layout:
# $PREFIX/spack
# $PREFIX/spack_config
# $PREFIX/spack_packages
# $PREFIX/release (defined in $PREFIX/spack_config/config.yaml)

# This file is located at $PREFIX/spack_config/$0

set -x
PREFIX="$(dirname $BASH_SOURCE)/.."
SPACK="$PREFIX/spack"
CONFIG="$PREFIX/spack_config/config"
set +x

# https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format
#
# When Spack checks its configuration, the configuration scopes are updated
# as dictionaries in increasing order of precedence, allowing higher precedence
# files to override lower. YAML dictionaries use a colon “:” to specify
# key-value pairs. Spack extends YAML syntax slightly to allow a double-colon
# “::” to specify a key-value pair. When a double-colon is used, instead of
# adding that section, Spack replaces what was in that section with the new
# value.

# Don't disable local config, we need to use SPACK_USER_CONFIG_PATH.
#export SPACK_DISABLE_LOCAL_CONFIG=""

# No need to override, because it defaults to a non-existent /etc/spack on Gadi.
#export SPACK_SYSTEM_CONFIG_PATH=""

# Override ~/.spack because we have seen compiler misconfiguration by users.
export SPACK_USER_CONFIG_PATH="$CONFIG"

# TODO: Decide on the version of Python that we approve.
#export SPACK_PYTHON=

. $SPACK/share/spack/setup-env.sh
