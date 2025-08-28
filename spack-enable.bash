# This is not an executable! Do not enable execute permissions.
# You need to be running a bash shell, then execute: . spack-enable.bash
# This file is from https://github.com/ACCESS-NRI/spack-config/

# Required layout:
# $prefix/spack
# $prefix/${CONFIGDIR}
# $prefix/spack-packages
# $prefix/release (defined in $prefix/${CONFIGDIR}/*/*/config.yaml)

# https://spack-tutorial.readthedocs.io/en/latest/tutorial_configuration.html#yaml-format
#
# When Spack checks its configuration, the configuration scopes are updated
# as dictionaries in increasing order of precedence, allowing higher precedence
# files to override lower. YAML dictionaries use a colon “:” to specify
# key-value pairs. Spack extends YAML syntax slightly to allow a double-colon
# “::” to specify a key-value pair. When a double-colon is used, instead of
# adding that section, Spack replaces what was in that section with the new
# value.

# TODO: Decide on the version of Python that we approve.
#export SPACK_PYTHON=

CONFIGDIR="$(realpath $(dirname $BASH_SOURCE))"

# NOTE: A lot of ugly code below to avoid setting variables in the
#       user's environment. e.g. Avoid defining functions.

if [ "$#" -eq 0 ]
then
    # Disable ~/.spack because we have seen compiler misconfiguration by
    # users. This also disables /etc/spack .
    export SPACK_DISABLE_LOCAL_CONFIG="true"

    # Setting SPACK_DISABLE_LOCAL_CONFIG ignores the following:
    # export SPACK_SYSTEM_CONFIG_PATH=""
    # export SPACK_USER_CONFIG_PATH=""
    unset SPACK_SYSTEM_CONFIG_PATH
    unset SPACK_USER_CONFIG_PATH
    echo "Using configuration in spack/etc/spack"

    # NOTE: If using symlinks is undesirable, the following commands can
    #       be used to construct the name of the relevant config directory.
    # git -C ${prefix}/spack branch
    # hostname --fqdn

# NOTE: This option is for build-ci
elif [[ "${1}" == "ci" || "${1}" == "ci-compiler-find" ]]
then
    unset SPACK_DISABLE_LOCAL_CONFIG
    echo "Using configuration in spack/etc/spack, with CI user config enabled"
else
    echo "Usage: . ${PROGNAME} [ci|ci-compiler-find]"
    unset CONFIGDIR
    return 1
fi


# https://github.com/spack/spack/issues/27704
export SPACK_USER_CACHE_PATH="${CONFIGDIR}/../"

. ${CONFIGDIR}/../spack/share/spack/setup-env.sh
unset CONFIGDIR

if [ "${1}" == "ci-compiler-find" ]
then
    upstream_compilers_file="${ENV_COMPILERS_SPACK_MANIFEST:-/opt/compilers.spack.yaml}"
    echo "Loading compilers from $upstream_compilers_file..."

    if [ ! -x "$(command -v yq)" ]; then
        echo "Error: yq is not installed, but needs to be for spack compiler lookup."
        unset upstream_compilers_file
        exit 1
    fi

    yq '.spack.specs[]' "$upstream_compilers_file" | while read -r compiler; do
        spack load "$compiler" || exit
        spack compiler find --scope=user
    done
    echo "Compilers loaded."
    unset upstream_compilers_file
fi
