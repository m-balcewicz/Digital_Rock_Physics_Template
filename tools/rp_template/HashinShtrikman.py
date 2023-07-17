# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Hashin-Shtrikman Bounds
# according to Hashin–Shtrikman–Walpole Bounds by Mavko, G., Mukerji, T.,
# Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)
#
# by Martin Balcewicz
# martin.balcewicz@rockphysics.org
# 01/2023
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #

# Example according to Mavko et al.: The Rock Physics Handbook. (2020)
# phase = ['Quartz', 'Calcite', 'Water']
# porosity=0.27

# all values in Pascal
# BULK_quartz=36e-9;
# BULK_calcite=75e-9;
# BULK_water=2.2e-9;
# bulk_modulus_mineral = (36e-9, 75e-9, 2.2e-9)

# SHEAR_quartz=45e-9;
# SHEAR_calcite=31e-9;
# SHEAR_water=0e-9;
# shear_modulus_mineral = (45e-9, 31e-9, 0)

# Fractions
# quartz=58.4%
# calcite=14.6%
# porosity=27%
# fraction = (0.584, 0.146, 0.27)


import numpy as np
import pandas as pd


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to Hashin-Shtrikman upper and lower boundary calculations')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to Hashin–Shtrikman–Walpole Bounds by')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def hashin_shtrikman_bounds(**kwargs):
    #     if K_max_phase != G_max_phase:
    #         print('INFO: Your set of minerals is not well-ordered:')
    #         explanation = '''The constituent with the largest bulk modulus has not the largest
    # shear modulus and the constituent with the smallest bulk modulus
    # also has not the smallest shear modulus. Within this range of
    # validity, the two-phase Hashin–Shtrikman bounds are not optimum. '''
    #         # , giving the narrowest possible range without specifying
    #         #  anything about the geometries of the constituents
    #         print(explanation)
    #         print('')
    #         print('')
    #         print('')
    #         well_ordered = False
    #     else:
    #         print('INFO: Your set of minerals is well-ordered.')
    #
    #         well_ordered = not False

    # # Upper Hashin-Shtrikman-Walpole Bound (Bulk Modulus)

    # z = (4 / 3) * G_max  # G_max is required
    # HSW_K_up =

    if 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs and 'fractions_rock' in kwargs:
        bulk_modulus_rock = kwargs.get('bulk_modulus_rock')
        shear_modulus_rock = kwargs.get('shear_modulus_rock')
        fractions_rock = kwargs.get('fractions_rock')
        G_max = np.max(shear_modulus_rock)
        G_min = np.min(shear_modulus_rock)
        K_max = np.max(bulk_modulus_rock)
        K_min = np.min(bulk_modulus_rock)
        # print(f'K_min: {K_min *1e-9} (GPa)')
        # print(f'G_max: {G_max * 1e-9} (GPa)')
        # print(f'K_max: {K_max *1e-9} (GPa)')
        # print(f'G_min: {G_min * 1e-9} (GPa)')

        # Upper Hashin-Shtrikman Bound (Bulk Modulus)
        z = (4 / 3) * G_max  # G_max is required
        var = np.zeros((len(bulk_modulus_rock), 1))
        for m in range(len(bulk_modulus_rock)):
            var[m] = fractions_rock[m] / (bulk_modulus_rock[m] + z)

        HS_K_up = float(1 / sum(var) - z)

        # Lower Hashin-Shtrikman Bound (Bulk Modulus)
        z = (4 / 3) * G_min  # G_min is required
        var = np.zeros((len(bulk_modulus_rock), 1))
        for m in range(len(bulk_modulus_rock)):
            var[m] = fractions_rock[m] / (bulk_modulus_rock[m] + z)

        HS_K_low = float(1 / sum(var) - z)

        # Upper Hashin-Shtrikman Bound (Shear Modulus)
        zeta = G_max / 6 * ((9 * K_max + 8 * G_max) / (K_max + 2 * G_max))
        var = np.zeros((len(bulk_modulus_rock), 1))
        for m in range(len(bulk_modulus_rock)):
            var[m] = fractions_rock[m] / (shear_modulus_rock[m] + zeta)

        HS_G_up = float(1 / sum(var)) - zeta

        # Lower Hashin-Shtrikman Bound (Shear Modulus)
        zeta = G_min / 6 * ((9 * K_min + 8 * G_min) / (K_min + 2 * G_min))
        var = np.zeros((len(bulk_modulus_rock), 1))
        for m in range(len(bulk_modulus_rock)):
            var[m] = fractions_rock[m] / (shear_modulus_rock[m] + zeta)

        HS_G_low = float(1 / sum(var)) - zeta

        return HS_K_low, HS_K_up, HS_G_up, HS_G_low


    else:
        print("Not enough information provided to calculate the elastic moduli")
        HS_K_low = 'nan'
        HS_K_up = 'nan'
        HS_G_low = 'nan'
        HS_G_up = 'nan'

        return HS_K_low, HS_K_up, HS_G_up, HS_G_low


# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
    # phase = ('Quartz', 'Feldspar', 'Dolomite', 'Calcite')
    # bulk_modulus_mineral = np.multiply([37, 75, 95, 76], 1e-9)
    # shear_modulus_mineral = np.multiply([44, 25, 45, 32], 1e-9)
    # fraction = (0.5, 0.3, 0.1, 0.1)
    # porosity = 0.1
    # HS_K_low, HS_K_up, HS_G_up, HS_G_low, well_ordered, K_max, G_max = hashin_shtrikman_bounds(porosity, phase,
    #                                                                                            fraction,
    #                                                                                            bulk_modulus_mineral,
    #                                                                                            shear_modulus_mineral)
    # round_factor = 4
    # print('Upper Hashin-Shtrikman Bound for Bulk Modulus:', round(HS_K_up / 1e-9, round_factor), 'GPa')
    # print('Lower Hashin-Shtrikman Bound for Bulk Modulus:', round(HS_K_low / 1e-9, round_factor), 'GPa')
    HS_K_low, HS_K_up, HS_G_up, HS_G_low = hashin_shtrikman_bounds(bulk_modulus_rock=[36e9, 75e9, 2.2e9], shear_modulus_rock=[45e9, 31e9, 0], fractions_rock=[(1-0.27)*0.8, (1-0.27)*0.2, 0.27])
    # print('Aggregates = 47.74%')
    print(f'HS K up: {HS_K_up * 1e-9} (GPa)')
    print(f'HS K low: {HS_K_low * 1e-9} (GPa)')
    print(f'HS G up: {HS_G_up * 1e-9} (GPa)')
    print(f'HS G low: {HS_G_low * 1e-9} (GPa)')
    print('')
    # print('Aggregates = 49.66%')
    # HS_K_low, HS_K_up, HS_G_up, HS_G_low = hashin_shtrikman_bounds(bulk_modulus_rock=[], shear_modulus_rock=[7.54e9, 37.77e9], fractions_rock=[0.4866, 0.4966])
    # print(f'HS K up: {HS_K_up * 1e-9} (GPa)')
    # print(f'HS K low: {HS_K_low * 1e-9} (GPa)')
    # print(f'HS G up: {HS_G_up * 1e-9} (GPa)')
    # print(f'HS G low: {HS_G_low * 1e-9} (GPa)')
