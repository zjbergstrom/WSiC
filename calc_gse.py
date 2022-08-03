'''
This code carries out the calculation of GSE
'''

import os
import ase

from pymatgen.io.ase import AseAtomsAdaptor
from ase.calculators.abinit import Abinit
from sympy import asec

import generate_files as gf
#import base_compounds as bc

'''
Takes in a pymatgen structure object
convert to ASE and calculates the GSE
using the Abinit calculator
'''
Ha2eV = 27.211
params = {"ecut" : int(60*Ha2eV),
            "toldfe" : 1e-6}
def calc_gse(structures):
    label = "abinit"
    os.system("rm abinit*")
    for structure in structures:
        ase_structure = AseAtomsAdaptor.get_atoms(structure)
        calc = Abinit(v8_legacy_format=True, atoms=ase_structure, label=label, param=params)
        ase_structure.calc = calc
        ase_structure.write_input()
        e = ase_structure.get_potential_energy()

if __name__=="__main__":
    #base = bc.getBaseElements()
    calc_gse(gf.getStructures(filename="filenames0.txt",dir="structurefiles/"))
