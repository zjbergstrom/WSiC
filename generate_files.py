'''
This code creates ipnut files for abinit calculations
'''
import os
import ase
from pymatgen.core import Lattice, Structure, Molecule, IStructure
from pymatgen.core.periodic_table import Element
#from pymatgen.ext.matproj import MPRester
from mp_api import MPRester
import pandas as pd

from ase.io.abinit import * #write_abinit_in, read_abinit_out, read_results
import ase.io.abinit as aseio
from pymatgen.io.ase import AseAtomsAdaptor

import base_compounds as bc
import slurm as sl
import ternary as tn

PP_PATH = os.environ["PP"]


Ha2eV = 27.211

USER_API_KEY = "N0fphWZIy7x6VtkvAEmshsCSdtEBZoQF"
#USER_API_KEY = "iItEHUSQ6meb9nks"
base = {"W":"mp-91","Si":"mp-149","C":"mp-569304"}

params = {"ecut" : int(60*Ha2eV),
            "toldfe" : 1e-6,
            "nstep" : 40,
            "kpts" : 1,
            "optcell" : 1,
            "ionmov" : 2,
            "ntime" : 10,
            "dilatmx" : 1.05,
            "ecutsm" : 0.5}


def writeFiles(structure):
    # Write *.files
    with open(structure.composition.reduced_formula + ".files","w") as fout:
        name = structure.composition.reduced_formula
        fout.write('./input/{}.in\n'.format(name))
        fout.write('./results/{}.out\n'.format(name))
        fout.write('./results/{}-i\n'.format(name))
        fout.write('./results/{}-o\n'.format(name))
        fout.write('./results/{}-x\n'.format(name))
        print(structure.composition.reduced_formula)
        for element in structure.composition.elements:
            print(element.symbol)
            fout.write('{}/LDA_FHI/{}-{}.LDA.fhi\n'.format(PP_PATH,element.symbol,element.Z))


def makeRunDirs(structure):
    name = structure.composition.reduced_formula
    os.system("mkdir simulations")
    os.system("mkdir simulations/{}".format(name))
    os.system("mkdir simulations/{}/input".format(name))
    os.system("mkdir simulations/{}/results".format(name))
    os.system("mv {}.files simulations/{}/input".format(name,name))
    os.system("mv {}.in simulations/{}/input".format(name,name))
    os.system("mv saturn.sbatch simulations/{}".format(name))


def generateInputs(structures):
    for structure in structures:

        # Information on structure
        print(structure.composition.formula)
        print(structure.get_space_group_info())

        # Change structure to ase type
        ase_structure = AseAtomsAdaptor.get_atoms(structure)
        print(type(ase_structure))

        # Write abinit.in
        with open(structure.composition.reduced_formula + ".in","w") as fd:
            write_abinit_in(fd, ase_structure, param=params)

        sl.writeSubmitScript(name=structure.composition.reduced_formula)
        writeFiles(structure)
        makeRunDirs(structure)

if __name__ == "__main__":
    generateInputs(bc.getBaseElements())
    # generateInputs(tn.getTernaryStructures())