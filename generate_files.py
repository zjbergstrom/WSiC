'''
This code creates ipnut files for abinit calculations
'''
import os
import ase
from pymatgen.core import Lattice, Structure, Molecule, IStructure
from pymatgen.core.periodic_table import Element
import pandas as pd

from ase.io.abinit import *
import ase.io.abinit as aseio
from pymatgen.io.ase import AseAtomsAdaptor

import slurm as sl
import structure_pathways as sp

PP_PATH = os.environ["PP"]
Ha2eV = 27.211
rundir = "simulations"

print("Putting files into directory: {}".format(rundir))

params = {"ecut" : int(60*Ha2eV),
            "toldfe" : 1e-6,
            "nstep" : 10,
            "kpts" : 1,
            "chksymbreak" : 0,
            "optcell" : 2,
            "ionmov" : 2,
            "ntime" : 10,
            "dilatmx" : 1.1,
            "ecutsm" : 0.5,
            # "getwfk" : -1,
}


def writeFiles(structure,PP):
    # Write *.files
    name = structure.composition.formula.replace(" ","")
    with open(name + ".files","w") as fout:
        fout.write('./input/{}.in\n'.format(name))
        fout.write('./results/{}.out\n'.format(name))
        fout.write('./results/{}-i\n'.format(name))
        fout.write('./results/{}-o\n'.format(name))
        fout.write('./results/{}-x\n'.format(name))
        for e in ["C","Si","W"]:
            for element in structure.composition.elements:
                if PP == "LDA_FHI":
                    if e==element.symbol:
                        if element.symbol == "C":
                            fout.write('{}/LDA_FHI/0{}-{}.LDA.fhi\n'.format(PP_PATH,element.Z,element.symbol))
                        else:
                            fout.write('{}/LDA_FHI/{}-{}.LDA.fhi\n'.format(PP_PATH,element.Z,element.symbol))
                elif PP == "psp8":
                    if e==element.symbol:
                        fout.write('{}/pbe_s_sr/{}.psp8\n'.format(PP_PATH,element.symbol))


def makeRunDirs(structure):
    name = structure.composition.formula.replace(" ","")
    os.system("mkdir {}/{}".format(rundir,name))
    os.system("mkdir {}/{}/input".format(rundir,name))
    os.system("mkdir {}/{}/results".format(rundir,name))

def mvFiles(structure):
    name = structure.composition.formula.replace(" ","")
    os.system("mv {}.files {}/{}/input".format(name,rundir,name))
    os.system("mv {}.in {}/{}/input".format(name,rundir,name))
    os.system("mv abinit.sbatch {}/{}".format(rundir,name))

def getStructures(struct_paths):
    structures = []
    for POSCARS in struct_paths:
        for poscar in POSCARS.keys():
            structure = Structure.from_file(POSCARS[poscar])
            print(structure.composition.formula.replace(" ",""), structure.get_space_group_info())
            structures.append(structure)
    return structures




data = {"structure" : [],
        "space group" : [],
        "W" : [],
        "Si" : [],
        "C" : [],
        }

def generateInputs(structures):
    os.system("mkdir {}".format(rundir))
    for structure in structures:

        # Information on structure
        name = structure.composition.formula.replace(" ","")
        print(name, structure.get_space_group_info())

        # Change structure to ase type
        ase_structure = AseAtomsAdaptor.get_atoms(structure)

        # Write abinit.in
        with open(name + ".in","w") as fd:
            write_abinit_in(fd, ase_structure, param=params)

        sl.writeSubmitScript(cluster="iris", script_name="abinit.sbatch", job_name=name, \
                                rundir=rundir, nodes=1, hrs=0, mins=30)
        writeFiles(structure,"LDA_FHI")
        makeRunDirs(structure)
        mvFiles(structure)

        # make dataframe as structure files are being populated
        data["structure"].append(name)
        data["space group"].append(structure.get_space_group_info())
        comp = structure.composition.get_el_amt_dict()
        data["W"].append(comp["W"])
        data["Si"].append(comp["Si"])
        data["C"].append(comp["C"])

                

if __name__ == "__main__":
    generateInputs(getStructures([sp.base_pathways, sp.all_pathways]))
    # generateInputs(getStructures(sp.findDict("DNF.txt")))

    # df = pd.DataFrame(data)
    # print(df)
    # df.to_pickle('structure_data.pkl')
