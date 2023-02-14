"""
Copyright 2022 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
SPDX-License-Identifier: Apache-2.0
"""

import argparse
import copy
import os
import re
import subprocess
import sys

import pdb
import yaml


def module(*args):
    """
    Run environment module command and capture all output, return as array of lines
    """
    cmd = ["modulecmd", "bash"] + list(args)
    return subprocess.run(cmd, capture_output=True).stderr.decode().splitlines()


def filter(list, string):
    """
    Filter list for entries that begin with string and remove trailing '(default)' string
    """
    return [f.removesuffix("(default)") for f in list if f.startswith(string)]


def parse_args(args):

    parser = argparse.ArgumentParser(
        description="Create a spack compilers.yml configuration file for gadi"
    )
    parser.add_argument(
        "-v", "--verbose", help="Increase verbosity", action="count", default=0
    )

    return parser.parse_args(args)


def find_modules(modstring, defdict, type="compiler", specstring=None, variants="", 
                 verbose=False, prefix=None):
    """
    Find all modules matching modstring, replace some values in defdict
    based on values from module to populate spack config files
    """
    modlist = []

    if specstring is None:
        specstring = modstring

    modules = filter(module("avail", "-t", modstring), modstring + "/")
    for mod in modules:
        if verbose:
            print(f"Adding {mod}")
        _, version = mod.rsplit("/", 1)
        # Only use modules with legit version number
        if not re.match(r"[\d.]+", version):
            continue
        moddict = copy.deepcopy(defdict)
        moddict["spec"] = f"{specstring}@{version}{variants}"
        moddict["modules"].append(mod)
        if type == "package":
            if prefix is not None:
                path_prefix = prefix.format(mod=mod, version=version)
            else:
                path_prefix = mod
            moddict["prefix"] += str(path_prefix)
            modlist.append(moddict)
        else:
            modlist.append({type: moddict})

    return modlist


def main(args):

    compilers = []

    # Intel compiler modules
    def_compiler_dict = {
        "spec": None,
        "paths": {
            "cc": "/apps/intel-ct/wrapper/icc",
            "cxx": "/apps/intel-ct/wrapper/icpc",
            "f77": "/apps/intel-ct/wrapper/ifort",
            "fc": "/apps/intel-ct/wrapper/ifort",
        },
        "flags": {},
        "operating_system": "rocky8",
        "target": "x86_64",
        "modules": [],
        "environment": {},
        "extra_rpaths": [],
    }

    modstring = "intel-compiler"
    compilers.extend(
        find_modules(
            modstring, def_compiler_dict, specstring="intel", verbose=args.verbose
        )
    )

    # Update paths for oneAPI compiler modules
    def_compiler_dict["paths"].update(
        {
            "cc": "/apps/intel-ct/wrapper/icx",
            "cxx": "/apps/intel-ct/wrapper/icp",
            "f77": "/apps/intel-ct/wrapper/ifx",
            "fc": "/apps/intel-ct/wrapper/ifx",
        }
    )

    modstring = "intel-compiler-llvm"
    compilers.extend(
        find_modules(
            modstring, def_compiler_dict, specstring="oneapi", verbose=args.verbose
        )
    )

    # Update paths for gcc modules
    def_compiler_dict["paths"].update(
        {
            "cc": "/opt/nci/wrappers/gcc",
            "cxx": "/opt/nci/wrappers/g++",
            "f77": "/opt/nci/wrappers/gfortran",
            "fc": "/opt/nci/wrappers/gfortran",
        }
    )

    modstring = "gcc"
    compilers.extend(find_modules(modstring, def_compiler_dict, verbose=args.verbose))

    # Write compilers.yaml file to local directory.  Note that this completely
    # overwrites the compilers.yaml file, it does not amend, or retain any
    # configuration information
    with open("compilers.yaml", "w") as outfile:
        yaml.dump(
            {"compilers": compilers},
            outfile,
            default_flow_style=False,
            sort_keys=False,
        )

    # Update externals from an existing packages.yaml file if it exists
    # and contains data
    externals = {"packages": {}}
    tmp = None
    try:
        with open("packages.yaml", "r") as pkgfile:
            tmp = yaml.safe_load(pkgfile)
    except FileNotFoundError:
        pass
    finally:
        if tmp is not None:
            externals.update(tmp)

    # External packages to search for available modules.
    # module_string: spec_string are key/value pairs
    external_packages = {
        "openmpi": "openmpi",
        "intel-mpi": "intel-mpi",
        "intel-mkl": "intel-mkl",
        "python3": "python",
        "cmake": "cmake",
        "git": "git",
    }

    variants = { "python": "+bz2+ctypes+dbm+lzma+nis+pyexpat~pythoncmd+readline+sqlite3+ssl+tix+tkinter+uuid+zlib"}

    def_package_dict = {
        "spec": None,
        "prefix": f"/apps/",
        "modules": [],
    }

    prefix_configure = {
        "intel-mkl": "intel/compilers_and_libraries_{version}/linux/mkl"
    }

    for modstring, specstring in external_packages.items():

        # Load package if it already exists, otherwise an empty dict
        package_dict = externals["packages"].get(specstring, {})
        # Replace the list of external packages, but retain other settings
        package_dict["externals"] = find_modules(
            modstring,
            def_package_dict,
            specstring=specstring,
            variants=variants.get(specstring, ""),
            type="package",
            verbose=args.verbose,
            prefix=prefix_configure.get(modstring, None)
        )

        # Update package
        externals["packages"][specstring] = package_dict

    with open("packages.yaml", "w") as pkgfile:
        yaml.safe_dump(
            data=externals, stream=pkgfile, default_flow_style=False, sort_keys=False
        )


def main_argv():

    args = parse_args(sys.argv[1:])

    main(args)


if __name__ == "__main__":

    main_argv()
