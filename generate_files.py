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

PP_PATH = os.environ["PP"]

Ha2eV = 27.211

rundir = "simulations"
print("Putting files into {}".format(rundir))

params = {"ecut" : int(60*Ha2eV),
            "toldfe" : 1e-6,
            "nstep" : 40,
            "kpts" : 1,
            "chksymbreak" : 0,
           "optcell" : 1,
           "ionmov" : 2,
           "ntime" : 10,
           "dilatmx" : 1.05,
           "ecutsm" : 0.5
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
    os.system("mv saturn.sbatch {}/{}".format(rundir,name))

def getStructures(filename,dir):
    #read the data
    instr=open(filename,'r')
    POSCARs=instr.readlines()

    structures = []
    for poscar in POSCARs:
        print("Loading ",poscar.strip())
        structure = Structure.from_file(dir + poscar.strip())
        print(structure.composition.formula)
        print(structure.get_space_group_info())
        structures.append(structure)

    return structures


# pandas df data structures
# W Si C
data = {"structure" : [],
        "space group" : [],
        "W" : [],
        "Si" : [],
        "C" : [],
        # "atom quantities" : [],
        }

def generateInputs(structures):
    os.system("mkdir {}".format(rundir))
    for structure in structures:

        # Information on structure
        name = structure.composition.formula.replace(" ","")
        print(name)
        print(structure.get_space_group_info())

        # Change structure to ase type
        ase_structure = AseAtomsAdaptor.get_atoms(structure)

        # Write abinit.in
        with open(name + ".in","w") as fd:
            write_abinit_in(fd, ase_structure, param=params)

        sl.writeSubmitScript(cluster="saturn", script_name="saturn.sbatch", job_name=name, \
                                rundir=rundir, nodes=None, cpus=None, hrs=0, mins=30)
        writeFiles(structure,"LDA_FHI")
        makeRunDirs(structure)
        mvFiles(structure)

        # make dataframe as structure files are being populated
        data["structure"].append(name)
        data["space group"].append(structure.get_space_group_info())
        comp = structure.composition.get_el_amt_dict()
        # data["atom quantities"].append([comp["W"],comp["Si"],comp["C"]])
        data["W"].append(comp["W"])
        data["Si"].append(comp["Si"])
        data["C"].append(comp["C"])

                

if __name__ == "__main__":
    generateInputs(getStructures(filename="filenames0.txt",dir="structurefiles/"))
    # generateInputs(getStructures(filename="filenames1.txt",dir="structurefiles/"))
    # generateInputs(getStructures(filename="filenames2.txt",dir="ternary_reference_compounds_structures/"))

    # generateInputs(getStructures(filename="DNF.txt",dir="structurefiles/"))

    df = pd.DataFrame(data)
    print(df)
    df.to_pickle('structure_data.pkl')
