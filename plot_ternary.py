"""An example of the colorbar display on the scatter plot."""
import ternary
import matplotlib.pyplot as plt
import numpy as np

def _en_to_enth(energy, concs, A, B, C):
    """Converts an energy to an enthalpy.
    Converts energy to enthalpy using the following formula:
    Enthalpy = energy - (energy contribution from A) - (energy contribution from B) -
        (energy contribution from C)
    An absolute value is taken afterward for convenience.
    
    Parameters
    ----------
    energy : float
        The energy of the structure
    concs : list of floats
        The concentrations of each element
    A : float
        The energy of pure A
    B : float
        The energy of pure B
    C : float
        The energy of pure C
    Returns
    -------
    enth : float
       The enthalpy of formation.
    """

    enth = energy - concs[0]*A - concs[1] * B - concs[2] * C
    return enth


def _energy_to_enthalpy(energy):
    """Converts energy to enthalpy.
    
    This function take the energies stored in the energy array and
    converts them to formation enthalpy.
    Parameters
    ---------
    energy : list of lists of floats
    
    Returns
    -------
    enthalpy : list of lists containing the enthalpies.
    """

    pureA = energy[0][0] / energy[0][1][0]
    pureB = energy[1][0] / energy[1][1][1]
    pureC = energy[2][0] / energy[2][1][2]

    enthalpy = []
    for en in energy:
        c = en[1]
        conc = [float(i) / sum(c) for i in c]

        VASP = _en_to_enth(en[0]/sum(c), conc, pureA, pureB, pureC)

        enthalpy.append([VASP, conc])

    return enthalpy


def _read_data(fname):
    """Reads data from file.
    Reads the data in 'fname' into a list where each list entry contains 
    [energy calculated, list of concentrations].
    Parameters
    ----------
    fname : str
        The name and path to the data file.
    
    Returns
    -------
    energy : list of lists of floats
       A list of the energies and the concentrations.
    """
    
    energy = []
    with open(fname,'r') as f:
        for line in f:
            VASP = abs(float(line.strip().split()[0]))
            conc = [i for i in line.strip().split()[1:]]

            conc_f = []
            for c in conc:
                conc_f.append(int(float(c)))
            energy.append([VASP, conc_f])
    return energy


def conc_plot(fname):
    """Plots the error in the CE data.
    
    This plots the error in the CE predictions within a ternary concentration diagram.
    Parameters
    ----------
    fname : string containing the input file name.
    """

    energies = _read_data(fname)
    enthalpy = _energy_to_enthalpy(energies)

    # print(enthalpy)

    points = []
    colors = []
    sizes = []
    for en in enthalpy:
        print(en[0])
        if en[0] < 1 and en[0] > -4:
            concs = en[1]
            points.append((concs[0] * 100, concs[1] * 100, concs[2] * 100))
            colors.append(en[0])
            sizes.append(en[0]*-1)

    maxi = max(sizes)
    mini = min(sizes)
    max_size = 40
    min_size = 2
    OldRange = maxi - mini  
    NewRange = max_size - min_size # max marker size minus min marker size
    marker_sizes = []
    for s in sizes:  
        marker_sizes.append((((s - mini) * NewRange) / OldRange) + min_size)

    # print("sizes",sizes)
    # print("marker sizes",marker_sizes)

    scale = 100
    figure, tax = ternary.figure(scale=scale)
    tax.boundary(linewidth=1.0)
    tax.set_title("Enthalpies", fontsize=20)
    tax.gridlines(multiple=10, color="blue")
    tax.scatter(points, vmax=max(colors), vmin=min(colors), marker='d', colormap=plt.cm.viridis, colorbar=True, c=colors, s=marker_sizes)
    tax.bottom_axis_label("W")
    tax.right_axis_label("Si")
    tax.left_axis_label("C")
    tax.get_axes().axis('off')
    tax.show()


if __name__ == "__main__":
    conc_plot('plot_data.txt')

