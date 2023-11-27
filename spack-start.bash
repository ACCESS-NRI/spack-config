# This is not an executable! Do not enable execute permissions.
# You need to be running a bash shell, then execute: . spack-start.bash
# This file is in $PREFIX/spack-config/

# Required layout:
# $PREFIX/spack
# $PREFIX/spack-config
# $PREFIX/spack-packages
# $PREFIX/release (defined in $PREFIX/spack-config/*/*/config.yaml)

set -x
PREFIX="$(dirname $BASH_SOURCE)/.."
SPACK="$PREFIX/spack"
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

# Disable ~/.spack because we have seen compiler misconfiguration by users.
# This also disables /etc/spack .
export SPACK_DISABLE_LOCAL_CONFIG="true"

# Setting SPACK_DISABLE_LOCAL_CONFIG disables the following:
#export SPACK_SYSTEM_CONFIG_PATH=""
#export SPACK_USER_CONFIG_PATH=""

# TODO: Decide on the version of Python that we approve.
#export SPACK_PYTHON=

. $SPACK/share/spack/setup-env.sh
