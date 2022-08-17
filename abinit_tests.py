from ase.calculators.abinit import Abinit
from ase.atoms import Atoms

atom = Atoms("W")
atom.calc = Abinit(ecut=200, toldfe=0.001)
atom.calc.write_input()
e = atom.calc.get_potential_energy()


