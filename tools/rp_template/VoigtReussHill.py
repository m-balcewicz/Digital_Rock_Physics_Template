# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Voigt and Reuss Bounds
# according to Voigt and Reuss Bounds and Voigt-Reuss-Hill Average by Mavko, G., Mukerji, T.,
# Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)
#
# by Martin Balcewicz
# martin.balcewicz@rockphysics.org
# 01/2023
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import numpy as np
import pandas as pd


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to Voigt-Reuss-Hill upper, lower, and average boundary calculations')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to Voigt upper and Reuss lower bound, and Voigt-Reuss-Hill average by')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def voigt_reuss_hill_bounds(phase, fraction, bulk_modulus_mineral, shear_modulus_mineral):
    fraction_control = 0
    while fraction_control > 1:
        print('Oops, please take a look to your fractions.')
        fraction_control = sum(fraction)

    if fraction == 'series':
        fraction_var = list(range(0, 101))
        fraction_var = fraction_var / 100
        properties = pd.DataFrame(
            {"Phase": phase, "Fraction": fraction_var[:], "K": bulk_modulus_mineral[:], "G": shear_modulus_mineral[:]})

        # Upper Voigt Bound (Bulk Modulus)
        var = np.zeros(len(properties), 1)
        Voigt_K = np.zeros(len(fraction_var), 1)
        for m in range(len(properties)):
            var[m] = properties.loc[m, "Fraction"] * (properties.loc[m, "K"])

        Voigt_K[m] = float(sum(var))

    else:
        properties = pd.DataFrame(
            {"Phase": phase, "Fraction": fraction[:], "K": bulk_modulus_mineral[:], "G": shear_modulus_mineral[:]})

    # Upper Voigt Bound (Bulk Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * (properties.loc[m, "K"])

    Voigt_K = float(sum(var))

    # Upper Voigt Bound (Shear Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * (properties.loc[m, "G"])

    Voigt_G = float(sum(var))

    # Lower Reuss Bound (Bulk Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] / (properties.loc[m, "K"])
    Reuss_K = float(1 / sum(var))

    # Lower Reuss Bound (Shear Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] / (properties.loc[m, "G"])
    Reuss_G = float(1 / sum(var))

    # Voigt-Reuss-Hill Average (Bulk Modulus)
    Voigt_Reuss_Hill_K = (Voigt_K + Reuss_K) / 2

    # Voigt-Reuss-Hill Average (Shear Modulus)
    Voigt_Reuss_Hill_G = (Voigt_G + Reuss_G) / 2

    return Voigt_K, Voigt_G, Reuss_K, Reuss_G, Voigt_Reuss_Hill_K, Voigt_Reuss_Hill_G


# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
