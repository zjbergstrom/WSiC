'''
This code calculates the GSE of the base elements
in the W-Si-C ternary system
'''
import os
import ase
from pymatgen.core import Lattice, Structure, Molecule, IStructure
from pymatgen.core.periodic_table import Species, Element, ElementBase
#from pymatgen.ext.matproj import MPRester
from mp_api import MPRester
import pandas as pd
import os
import calc_gse as cg

USER_API_KEY = "N0fphWZIy7x6VtkvAEmshsCSdtEBZoQF"
base = {"W":"mp-91","Si":"mp-149","C":"mp-569304"}


def getBaseElements():
    structures = []
    with MPRester(USER_API_KEY) as m:
        for element in base.keys():
            print(element)

            # Structure for material id
            structure = m.get_structure_by_material_id(base[element])
            structures.append(structure)

            #data = m.get_entry_by_material_id(base[element])
            #print(data)

            # To get a list of data for all entries having formula Fe2O3
            # data = m.get_data("Fe2O3")

            # To get the energies of all entries having formula Fe2O3
            # energies = m.get_data("Fe2O3", "energy")
    return structures

def pullGSE():
    base = {"W":"mp-91","Si":"mp-149","C":"mp-569304"}
    with MPRester(USER_API_KEY) as m:
        for element in base.keys():
            print(element)

            # Structure for material id
            structure = m.get_structure_by_material_id("mp-91")

            # Dos for material id
            #dos = m.get_dos_by_material_id("mp-91")

            # Bandstructure for material id
            #bandstructure = m.get_bandstructure_by_material_id("mp-91")

            # To get a list of data for all entries having formula Fe2O3
            # data = m.get_data("Fe2O3")

            # To get the energies of all entries having formula Fe2O3
            # energies = m.get_data("Fe2O3", "energy")

if __name__ == "__main__":
    os.system('clear')
    structures = getBaseElements()
    cg.calc_gse(structures)
    