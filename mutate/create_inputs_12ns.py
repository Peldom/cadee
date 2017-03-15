#!/usr/bin/env python
"""
This module generates Q-input files.

Author: {0} ({1})

This program is part of CADEE, the framework for
Computer-Aided Directed Evolution of Enzymes.
"""


from __future__ import print_function

import logging
import tarfile
import os

import tools

__author__ = "Beat Amrein"
__email__ = "beat.amrein@gmail.com"

logger = logging.getLogger('create_inputs')


templatetar = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'lib/template_12ns.tar.bz2')

if not os.path.isfile(templatetar):
    raise Exception('Template-Tar does not exist:', templatetar)

tarfile = tarfile.open(templatetar, mode='r:bz2')

# def status():
#    print("{0} {1} #SOLUTE".format(*solute_range))
#    print("{0} {1} #SOLVENT".format(*solvent_range))
#    for feprange in fepranges:
#        print("{0} {1} #FEPREGION".format(*feprange))


# fep settings
fep = "0.5 1 0"   # (seq restraints)

# warmup settings   (seq restraints)
dyn = [None]*9
dyn[1] = ("200 1 0", "20 1 0")
dyn[2] = ("200 1 0", "10 1 0")
dyn[3] = ("20 1 0", "5 1 0")
dyn[4] = ("20 1 0", "5 1 0")
dyn[5] = ("20 1 0", "2 1 0")
dyn[6] = ("5 1 0",)
dyn[7] = ("0.5 1 0",)


def create_inputs():
    def rewrite_res_section(base, fil=None):
        # for line in inpfil:
        #    if line.strip() == '[Sequence_Restraints]':
        #        break
        #    print(line, end='', file=fil)
        # print('[Sequence_Restraints]', file=fil)
        if "_dyn" in base and '08_dyn' not in base:
            idx = int(base[:2])
            print("  {1} {2}              {0}".format(
                dyn[idx][0], *solute_range), file=fil)
            if len(dyn[idx]) == 2:
                print("  {1} {2}           {0}".format(
                    dyn[idx][1], *solvent_range), file=fil)
        else:
            for feprange in reversed(fepranges):
                print("  {1} {2}           {0}".format(
                    fep, *feprange), file=fil)
        print('', file=fil)
        print('', file=fil)
        fil.close()

    pdbfil = 'mutant.pdb'
    fepfil = 'mutant.fep'

    if not os.path.isfile(pdbfil):
        errmsg = 'PDBFile {0} does not exist: {1}'.format(pdbfil, os.getcwd())
        raise Exception(errmsg)

    if not os.path.isfile(fepfil):
        errmsg = 'FEPFile {0} does not exist: {1}'.format(fepfil, os.getcwd())
        raise Exception(errmsg)

    # determine the ranges for solute, solvent, and fepatoms
    solute_range, solvent_range = tools.get_solute_and_solvent_ranges(pdbfil)
    indexes = tools.get_fep_atom_pdbindexes(fepfil)
    fepranges = tools.get_ranges(indexes)

    tarfile.extractall()
    for inp in os.listdir('.'):
        if inp[-4:] == ".inp":
            if "_eq" in inp or "_fep" in inp or "_dyn" in inp:
                base = os.path.basename(inp)
                rewrite_res_section(base, open(inp, 'a'))


def walk(folder):
    """ Walk trough subfolders and create inputs"""
    wd = os.getcwd()
    os.chdir(folder)
    for fol in os.listdir('.'):
        os.chdir(folder)
        logger.info('Create inputs for %s', fol)
        try:
            os.chdir(fol)
        except:
            continue
            # TODO: 4670_fep.inp has to be adjusted to a dummy file,
            #               that is written last, like z_allinputs
            if os.path.exists('4670_fep.inp'):
                logger.info('Skipping %s', fol)
                continue
        try:
            create_inputs()
        except Exception as e:
            # TODO: Errorhandling
            logger.warning('Exception %s happened in %s.', e, fol)
            raise
    os.chdir(wd)
