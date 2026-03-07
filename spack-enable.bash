# This is NOT an executable! Do not enable execute permissions.
# You need to be running a bash shell, then execute: . spack-enable.bash
# This file is from https://github.com/ACCESS-NRI/spack-config/

# Required layout:
# $prefix/spack
# $prefix/${CONFIGDIR}

# https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format
#
# When Spack checks its configuration, the configuration scopes are updated
# as dictionaries in increasing order of precedence, allowing higher precedence
# files to override lower. YAML dictionaries use a colon “:” to specify
# key-value pairs. Spack extends YAML syntax slightly to allow a double-colon
# “::” to specify a key-value pair. When a double-colon is used, instead of
# adding that section, Spack replaces what was in that section with the new
# value.

# https://spack.readthedocs.io/en/latest/configuration.html#configuration-scopes
# $ spack config scopes -p
# Scope           Path
# command_line
# spack           $spack/etc/spack/
# user            $HOME/spack/1.1
# site            $spack/etc/spack/site/
# system          $spack/../spack-config/<version>/<site>/
# defaults        $spack/etc/spack/defaults/
# defaults:linux  $spack/etc/spack/defaults/linux/
# defaults:base   $spack/etc/spack/defaults/base/
# _builtin


# TODO: Decide on the version of Python that we approve.
#export SPACK_PYTHON=

CONFIGDIR="$(realpath $(dirname $BASH_SOURCE))"

# NOTE: Try to avoid setting variables in the user's environment.

if [ "$#" -eq 0 ]
then
    # Setting SPACK_DISABLE_LOCAL_CONFIG ignores the following:
    # export SPACK_SYSTEM_CONFIG_PATH=""
    # export SPACK_USER_CONFIG_PATH=""
    # However, we want to allow the user to use these environment variables.
    unset SPACK_SYSTEM_CONFIG_PATH
    unset SPACK_USER_CONFIG_PATH
else
    echo "Usage: . ${PROGNAME}"
    unset CONFIGDIR
    return 1
fi

. ${CONFIGDIR}/../spack/share/spack/setup-env.sh
unset CONFIGDIR
