from pymatgen.core import Structure

def makeDict(filename,dir):
    struct_pathways = {}
    instr=open(filename,'r')
    POSCARs=instr.readlines()

    for poscar in POSCARs:
        file_dir = dir+poscar.strip()
        structure = Structure.from_file(file_dir)
        struct_pathways[structure.composition.formula.replace(" ","")] = file_dir

    return struct_pathways

def findDict(filename):
    struct_pathways = {}
    instr=open(filename,'r')
    structs=instr.readlines()

    for struct in structs:
        struct_pathways[struct] = all_pathways[struct]

    return struct_pathways

if __name__ == "__main__":

    makeDict(filename="filenames0.txt",dir="structurefiles/")
    makeDict(filename="filenames1.txt",dir="structurefiles/")
    makeDict(filename="filenames2.txt",dir="ternary_reference_compounds_structures/")
    

base_pathways = {
'W1': 'structurefiles/POSCAR._base_mpid=mp-91_formula=W1', 
'Si2': 'structurefiles/POSCAR._base_mpid=mp-149_formula=Si2', 
'C4': 'structurefiles/POSCAR._base_mpid=mp-569304_formula=C4'}

all_pathways = {
'W1': 'structurefiles/POSCAR._base_mpid=mp-91_formula=W1', 
'Si2': 'structurefiles/POSCAR._base_mpid=mp-149_formula=Si2', 
'C4': 'structurefiles/POSCAR._base_mpid=mp-569304_formula=C4',
'Si1W2': 'structurefiles/POSCAR._base_mpid=mp-1008625_formula=Si1 W2', 
'W2C1': 'structurefiles/POSCAR._base_mpid=mp-1008625_formula=W2 C1', 
'Si1W1': 'structurefiles/POSCAR._base_mpid=mp-1894_formula=Si1 W1', 
'W1C1': 'structurefiles/POSCAR._base_mpid=mp-1894_formula=W1 C1', 
'Si1W6C3': 'structurefiles/POSCAR._base_mpid=mp-1079377_formula=Si1 W6 C3', 
'Si2W6C2': 'structurefiles/POSCAR._base_mpid=mp-1079377_formula=Si2 W6 C2', 
'Si3W6C1': 'structurefiles/POSCAR._base_mpid=mp-1079377_formula=Si3 W6 C1', 
'Si4W6': 'structurefiles/POSCAR._base_mpid=mp-1079377_formula=Si4 W6', 
'C2': 'structurefiles/POSCAR._base_mpid=mp-149_formula=C2', 
'Si1C1': 'structurefiles/POSCAR._base_mpid=mp-149_formula=Si1 C1', 
'Si1W1C1': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1228818_formula=Si1 W1 C1', 
'Si2W1': 'structurefiles/POSCAR._base_mpid=mp-1620_formula=Si2 W1', 
'W1C2': 'structurefiles/POSCAR._base_mpid=mp-1620_formula=W1 C2', 
'Si1W8C3': 'structurefiles/POSCAR._base_mpid=mp-2034_formula=Si1 W8 C3', 
'Si2W8C2': 'structurefiles/POSCAR._base_mpid=mp-2034_formula=Si2 W8 C2', 
'Si3W8C1': 'structurefiles/POSCAR._base_mpid=mp-2034_formula=Si3 W8 C1', 
'W8C4': 'structurefiles/POSCAR._base_mpid=mp-2034_formula=W8 C4', 
'Si1W10C5': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si1 W10 C5', 
'Si2W10C4': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si2 W10 C4', 
'Si3W10C3': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si3 W10 C3', 
'Si4W10C2': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si4 W10 C2', 
'Si5W10C1': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si5 W10 C1', 
'Si6W10': 'structurefiles/POSCAR._base_mpid=mp-31219_formula=Si6 W10', 
'Si1W4C1': 'structurefiles/POSCAR._base_mpid=mp-33065_formula=Si1 W4 C1', 
'Si2W4': 'structurefiles/POSCAR._base_mpid=mp-33065_formula=Si2 W4', 
'W4C2': 'structurefiles/POSCAR._base_mpid=mp-33065_formula=W4 C2', 
'Si1W6C2': 'structurefiles/POSCAR._base_mpid=mp-567397_formula=Si1 W6 C2', 
'Si2W6C1': 'structurefiles/POSCAR._base_mpid=mp-567397_formula=Si2 W6 C1', 
'W6C3': 'structurefiles/POSCAR._base_mpid=mp-567397_formula=W6 C3', 
'Si1C3': 'structurefiles/POSCAR._base_mpid=mp-569304_formula=Si1 C3', 
'Si2C2': 'structurefiles/POSCAR._base_mpid=mp-569304_formula=Si2 C2', 
'Si3C1': 'structurefiles/POSCAR._base_mpid=mp-569304_formula=Si3 C1', 
'Si1W3': 'structurefiles/POSCAR._base_mpid=mp-979413_formula=Si1 W3', 
'W3C1': 'structurefiles/POSCAR._base_mpid=mp-979413_formula=W3 C1', 
'Si1W18C7': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=Si1 W18 C7', 
'Si3W18C5': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=Si3 W18 C5', 
'Si4W18C4': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=Si4 W18 C4', 
'Si5W18C3': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=Si5 W18 C3', 
'Si7W18C1': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=Si7 W18 C1', 
'W18C8': 'structurefiles/POSCAR._base_mpid=mp-684989_formula=W18 C8', 
'Si1W3C5': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si1 W3 C5', 
'Si2W3C4': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si2 W3 C4', 
'Si3W3C3': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si3 W3 C3', 
'Si4W3C2': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si4 W3 C2', 
'Si5W3C1': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si5 W3 C1', 
'Si6W3': 'structurefiles/POSCAR._base_mpid=mp-8939_formula=Si6 W3', 
'Si1W2C5': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si1 W2 C5', 
'Si2W2C4': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si2 W2 C4', 
'Si3W2C3': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si3 W2 C3', 
'Si4W2C2': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si4 W2 C2', 
'Si5W2C1': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si5 W2 C1', 
'Si6W2': 'structurefiles/POSCAR._base_mpid=mp-972748_formula=Si6 W2', 
'Si2W4C2': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1079892_formula=Si2 W4 C2', 
'Si1W2C3': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1216260_formula=Si1 W2 C3', 
'Si1W1C2': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1228830_formula=Si1 W1 C2', 
'Si3W1C4': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1228936_formula=Si3 W1 C4', 
'Si4W1C5': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1217128_formula=Si4 W1 C5', 
'Si1W3C4': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1228839_formula=Si1 W3 C4', 
'Si3W3C4': 'ternary_reference_compounds_structures/POSCAR._base_mpid=mp-1228977_formula=Si3 W3 C4'}