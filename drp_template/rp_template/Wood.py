# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Wood's Formula
# In a fluid suspension or fluid mixture, where the heterogeneity are small compared with a
# wavelength, the sound velocity is given exactly by Wood’s (1955) relation according to Mavko, G.,
# Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)
#
# by Martin Balcewicz
# martin.balcewicz@rockphysics.org
# 01/2023
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import numpy as np
import pandas as pd
import math


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to Wood\'s Formular calculations')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to Hashin–Shtrikman–Walpole Bounds by')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def wood(porosity, phase, fraction, bulk_modulus_mineral, density):
    properties = pd.DataFrame({"Phase": phase, "Fraction": fraction[:], "Density": density[:], "K": bulk_modulus_mineral[:]})

    # Reuss (isostress) average
    try:
        Reuss_K
    except NameError:
        var = np.zeros((len(properties), 1))
        for m in range(len(properties)):
            var[m] = properties.loc[m, "Fraction"] / (properties.loc[m, "K"])

        Reuss_K = float(1 / sum(var))

    else:
        Reuss_K = Reuss_K

    # Density average
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * (properties.loc[m, "Density"])

    rho_average = float(sum(var))

    # P-wave velocity
    Wood_VP_wet = math.sqrt(Reuss_K / rho_average) / 1e-9

    return rho_average, Wood_VP_wet, Reuss_K


# ------------------------------------------------------------------------------------------------- #
# # Example-1
# phase = ['Quartz', 'Water']
# bulk_modulus_mineral = (36e-9, 2.2e-9)
# fraction = (0.6, 0.4)
# density = (2650, 1000)  # kg/m^3
# porosity = 0.4

# Example-2
phase = ['Quartz', 'Water', 'Air']
bulk_modulus_mineral = (36e-9, 2.2e-9, 0.000131e-9)
porosity = 0.4
fraction = (1-porosity, 0.5*porosity, 0.5*porosity)
density = (2650, 1000, 0.00119/1e-3)  # kg/m^3


rho_average, Wood_VP_wet, Reuss_K = wood(porosity, phase, fraction, bulk_modulus_mineral, density)

if __name__ == '__main__':
    main()
    print('Reuss average for bulk modulus (Reuss_K):', Reuss_K / 1e-9, 'GPa')
    print('Density average of the suspension (rho_average):', round(rho_average, 2), 'kg/m^3')
    print('Wood\'s P-wave velocity (Wood_VP_wet):', round(Wood_VP_wet), 'm/s')
