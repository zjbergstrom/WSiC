
from ase import Atoms
from ase.calculators.emt import EMT



def singleAtomEnergy(atoms):
    '''
    Calculates single atom energies with Abinit
    
    Parameters
    ----------
    atoms : list of str
        The atoms to calculate ground state energy

    Returns
    -------
    gse : list of floats
       The ground state energy for each atom, in a vacuum
    '''
    for atom in atoms:
        a = Atoms(atom)
        a.center(vacuum=3.0)
        a.calc = EMT()
        e = a.get_potential_energy()
        print(atom,e)


if __name__ == "__main__":
    singleAtomEnergy(["H","C","N","O"])