'''
This code carries out the calculation of GSE
'''

import os
import ase

from pymatgen.io.ase import AseAtomsAdaptor
from ase.calculators.abinit import Abinit

import base_compounds as bc

'''
Takes in a pymatgen structure object
convert to ASE and calculates the GSE
using the Abinit calculator
'''
def calc_gse(structures):
    label = "abinit"
    os.system("rm abinit*")
    for structure in structures:
        ase_structure = AseAtomsAdaptor.get_atoms(structure)
    calc = Abinit(atoms=ase_structure,label=label,ecut=60)
    ase_structure.calc = calc
    e = ase_structure.get_potential_energy()

if __name__=="__main__":
    base = bc.getBaseElements()
    calc_gse([base[1]])
