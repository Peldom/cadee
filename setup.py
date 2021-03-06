from __future__ import print_function

"""
CADEE: Computer-Aided Directed Enzyme Evolution

To install CADEE type: "python setup.py install"
or for a single user "python setup.py install --user"

Author: {0} ({1})

This program is part of CADEE, the framework for
Computer-Aided Directed Evolution of Enzymes.

"""

from setuptools import setup

import os
import sys
from glob import glob

__author__ = "Beat Amrein"
__email__ = "beat.amrein@gmail.com"

execfile('cadee/version.py')

import cadee.executables.exe as exe

print('Welcome to CADEE Pre-Setup Check.')
print()

QEXES=['Qdyn6', 'Qprep6', 'Qfep6', 'Qcalc6']
qexedir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cadee/executables/q/')

def installation_failed():
    """
    Abort the setup/installation process.
    """
    print('')
    print('CADEE installation has failed.')
    import sys
    sys.exit(1)

def q_missing(exe):
    """
    Print message about the missing Q6-executable and call installation_failed.
    """
    print()
    print('ERROR: Could not find {0}. Please install Q6.'.format(exe))
    print("")
    print('       Copy the binaries to {0}.'.format(qexedir))
    print('       -OR-')
    print('       Ensure the binaries are in $PATH.'.format(exe))
    print()
    print('       Q6 can be obtained free of charge from {0}.'.format('https://github.com/qusers/Q6'))
    installation_failed()

if not (sys.version_info[0] == 2 and sys.version_info[1] == 7):
    print('Need Python 2.7')
    installation_failed()

# There are many versions of executables named Qdyn6.
# CADEE should stick to one version, so include with the cadee installation.
for qexe in QEXES:
    if not exe.which(qexe, True):

        print('Warning: Could not find {0} in {1}'.format(qexe, qexedir))
        print('         Searching in $PATH...')
        print()
        if exe.which(qexe):
            print('         Found {0} in {1}.'.format(qexe, exe.which(qexe)))
            print()
            print('         Will now copy {0} to {1}.'.format(qexe, qexedir))

            # compatibility of python3 and python2
            try:
                input = raw_input
            except NameError:
                pass
            ans = input('           Proceed (y/N)?').lower()

            if ans == 'y':
                print('         Proceed.')
                import shutil
                shutil.copy2(exe.which(qexe), qexedir)
                print('cped {0} to {1}.'.format(exe.which(qexe), qexedir))
            else:
                print('         Abort.')
                print('         Fatal: Cannot continue installation without {0}'.format(qexe))
                q_missing(qexe)
        else:
            print('Fatal: Could not find {0} in $PATH.'.format(qexe))
            q_missing(qexe)

if not exe.which('babel'):
    print('ERROR: Could not find babel. Please install Open Babel and ensure the binaries are in $PATH.')
    print('       Using Ubuntu try:  sudo apt-get install openbabel')
    print('       for Homebrew try:  brew install open-babel')
    installation_failed()

if not exe.which('Scwrl4'):
    print('ERROR: Scwrl4 is missing. Please install Scwrl4 and make sure the binary is in $PATH.')
    print()
    print('       Scwrl4 can be obtained from {0} (free for non-commercial use).'.format('http://dunbrack.fccc.edu/scwrl4/'))
    installation_failed()


setup(name='cadee',
      version=__version__,
      description='Computer Aided Directed Evolution of Enzymes',
      url='http://github.com/kamerlinlab/cadee',
      author='Beat Anton Amrein',
      author_email='beat.amrein@gmail.com',
      license='GPLv2',
      packages=['cadee', 'cadee.ana', 'cadee.dyn', 'cadee.prep', 'cadee.executables', 'cadee.qscripts', 'cadee.tools' ],
      py_modules=['cadee'],
      package_data={'cadee': ['lib/*', 'qscripts/lib/*', 'qscripts/REAMDE.md', 'qscripts/LICENSE.txt', 'executables/q/q*', 'tools/*', 'version.py']},
      install_requires=[
          ['mpi4py==1.3.1'],
          ['numpy'],
      ],
      scripts={
            'cadee/cadee',
      },
      zip_safe=False)
