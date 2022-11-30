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
    Run environment module command and capture all output
    """
    cmd = ['modulecmd', 'bash'] + list(args)
    return subprocess.run(cmd, capture_output=True).stderr.decode().splitlines()


def filter(list, string):
    """
    Filter list for entries that begin with string. Also
    remove trailing '(default)' string
    """
    return([f.removesuffix('(default)') for f in list if f.startswith(string)])

def parse_args(args):

    parser = argparse.ArgumentParser(description="Create a spack compilers.yml configuration file for gadi")
    parser.add_argument("-v","--verbose", help="Increase verbosity", action='count', default=0)

    return parser.parse_args(args)


def find_modules(modstring, defdict, type='compiler', specstring=None, verbose=False):
    """
    Find all modules matching modstring, replace some values in defdict
    based on values from module to populate spack config files
    """
    modlist = []

    if specstring is None:
        specstring = modstring

    modules = filter(module('avail', '-t', modstring), modstring + '/')
    for mod in modules:
        if verbose:
            print(f'Adding {mod}')
        _, version = mod.rsplit('/', 1)
        # Only use modules with legit version number
        if not re.match(r'[\d.]+', version):
            continue
        moddict = copy.deepcopy(defdict)
        moddict['spec'] = f'{specstring}@{version}'
        moddict['modules'].append(mod) 
        if type == 'package':
            moddict['prefix'] += mod
            modlist.append(moddict)
        else:
            modlist.append({type: moddict})

    return modlist


def main(args):

    compilers = []

    # Intel compiler modules
    def_compiler_dict = {
        'spec': None,
        'paths': {
            'cc' : '/apps/intel-ct/wrapper/icc',
            'cxx': '/apps/intel-ct/wrapper/icpc',
            'f77': '/apps/intel-ct/wrapper/ifort',
            'fc' : '/apps/intel-ct/wrapper/ifort',
        },
        'flags': {},
        'operating_system': 'rocky8',
        'target': 'x86_64',
        'modules': [],
        'environment': {},
        'extra_rpaths': [],
    }

    modstring = 'intel-compiler'
    compilers.extend(find_modules(modstring, def_compiler_dict, verbose=args.verbose))

    # Update paths for oneAPI compiler modules
    def_compiler_dict['paths'].update({ 
        'cc' : '/apps/intel-ct/wrapper/icx',
        'cxx': '/apps/intel-ct/wrapper/icp',
        'f77': '/apps/intel-ct/wrapper/ifx',
        'fc' : '/apps/intel-ct/wrapper/ifx',
        }
    )

    modstring = 'intel-compiler-llvm'
    compilers.extend(find_modules(modstring, def_compiler_dict, specstring='oneapi', verbose=args.verbose))

    # Update paths for gcc modules
    def_compiler_dict['paths'].update({ 
        'cc' : '/opt/nci/wrappers/gcc',
        'cxx': '/opt/nci/wrappers/g++',
        'f77': '/opt/nci/wrappers/gfortran',
        'fc' : '/opt/nci/wrappers/gfortran',
        }
    )

    modstring = 'gcc'
    compilers.extend(find_modules(modstring, def_compiler_dict, verbose=args.verbose))

    with open('compilers.yaml', 'w') as outfile:
        print(yaml.dump({'compilers': compilers}, outfile, default_flow_style=False, sort_keys=False))

    externals = {'packages': {}}
    with open('packages.yaml', 'r') as pkgfile:
        tmp = yaml.safe_load(pkgfile)
    if tmp is not None:
        externals.update(tmp)

    external_packages = {
            'openmpi': 'openmpi', 
            'intel-mpi': 'intel-mpi',
            'intel-mkl': 'intel-mkl',
            'python3': 'python',
            'cmake': 'cmake',
            'git': 'git',
            }

    for modstring, specstring in external_packages.items():

        def_package_dict = {
            'spec': None,
            'prefix': f'/apps/', 
            'modules': [],
        }

        # Load package if it already exists, otherwise an empty dict
        package_dict = externals['packages'].get(specstring, {})
        package_dict['externals'] = find_modules(modstring, 
                                                 def_package_dict, 
                                                 specstring=specstring, 
                                                 type='package', 
                                                 verbose=args.verbose)

        # Update package
        externals['packages'][specstring] = package_dict

    with open('packages.yaml', 'w') as pkgfile:
        yaml.safe_dump(data=externals, stream=pkgfile, default_flow_style=False, sort_keys=False)

    # print(yaml.safe_dump(externals, default_flow_style=False, sort_keys=False))

def main_argv():
    
    args = parse_args(sys.argv[1:])

    main(args)


if __name__ == "__main__":

    main_argv()