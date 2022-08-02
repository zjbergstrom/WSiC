import ase
from pymatgen.core import Lattice, Structure, Molecule, IStructure, composition
from pymatgen.core.periodic_table import Species, Element, ElementBase
#from pymatgen.core.composition import Composition
#from pymatgen.ext.matproj import MPRester
from mp_api import MPRester
import pandas as pd
import os

import calc_gse

USER_API_KEY = "N0fphWZIy7x6VtkvAEmshsCSdtEBZoQF"

# take in reference structures
# permutate through W, Si, C
# calculate gs energy
# add to ternary diagram
# record data in a pandas dataframe
'''
Looking over MAX phase compounds, which have the general form of:
M_(n+1) A X_(n)
where M is a transition metal
A is a group A element (ie Si)
X is a nitride or carbide
These are repeating structures
'''
# Looping over MAX phase compounts 

def getTernaryStructures(filename):
    #read the data
    #os.system("ls ternary_reference_compounds_structures > filenames.txt")
    instr=open(filename,'r')
    POSCARs=instr.readlines()

    base = [Element("W"),Element("Si"),Element("C")]
    structures = []
    for poscar in POSCARs:
        print("Loading ",poscar.strip())
        structure = Structure.from_file("ternary_reference_compounds_structures/" + poscar.strip())
        print(structure.composition.formula)
        print(structure.get_space_group_info())
        #print(structure.lattice)
        #print(structure.species)
        #print(structure.sites)
        #structure.replace(0,Element("H"))
        #print(type(structure.sites[0]))
        structures.append(structure)

    return structures


if __name__ == "__main__":
    structures = getTernaryStructures(filename="filenames1.txt")
