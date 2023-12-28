# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Seismic Wave Propagation, seismic velocity for isotropic, linear, elastic media according to
# Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)
#
# by Martin Balcewicz
# martin.balcewicz@rockphysics.org
# 01/2023
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import math


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome Seismic Velocity calculations for isotropic, linear, elastic media')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to ')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def velocity(rho_rock, **kwargs):
    # P-wave velocity
    if 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')
        G_rock = kwargs.get('shear_modulus_rock')
        p_wave_velocity = math.sqrt(
            ((K_rock * 1e9) + 4 / 3 * (G_rock * 1e9)) / (rho_rock / 1000)) * 1000
        statement_1 = "according to bulk modulus, shear modulus, and density"
        # print(statement_1)
        print(f"vP: {p_wave_velocity} (m/s; {statement_1})")

        # # based on calculated Lamé’s coefficients
        # lame_coef = K_rock - 2/3 * G_rock
        # # L_mu = G_rock
        # G_rock = kwargs.get('G_rock')
        # p_wave_velocity = math.sqrt((lame_coef + 2 * G_rock * 1e9) / density / 1000)
        # statement_2 = "According to Lamé’s coefficient, shear modulus, and density."
        # print(f"vP: {p_wave_velocity} (m/s; {statement_2})")

    elif 'lame_coef' in kwargs and 'shear_modulus_rock' in kwargs:
        lame_coef = kwargs.get('lame_coef')
        G_rock = kwargs.get('G_rock')
        p_wave_velocity = math.sqrt((lame_coef + 2 * G_rock * 1e9) / rho_rock / 1000)
        statement_1 = "According to Lamé’s coefficient, shear modulus, and density."
        print(f"vP: {p_wave_velocity} (m/s; {statement_1})")

    else:
        print("Not enough information provided to calculate the P-wave velocity.")
        p_wave_velocity = 'nan'

    # S-wave velocity
    if 'shear_modulus_rock' in kwargs:
        G_rock = kwargs.get('shear_modulus_rock')
        shear_wave_velocity = math.sqrt((G_rock * 1e9) / (rho_rock / 1000)) * 1000
        statement_1 = "according to shear modulus, and density"
        print(f"vS: {shear_wave_velocity} (m/s; {statement_1})")
    else:
        print("Not enough information provided to calculate the S-wave velocity.")
        shear_wave_velocity = 'nan'

    # extensional wave velocity
    if 'youngs_modulus_rock' in kwargs:
        E_rock = kwargs.get('youngs_modulus_rock')
        extensional_wave_velocity = math.sqrt(E_rock / rho_rock) * 1000
        statement_1 = "According to Young's modulus, and density."
        print(f"vE: {extensional_wave_velocity} (m/s; {statement_1})")
    elif 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')
        G_rock = kwargs.get('shear_modulus_rock')
        E_rock_cal = (9 * K_rock * 1e9 * G_rock * 1e9) / (3 * K_rock * 1e9 + G_rock * 1e9)
        extensional_wave_velocity = math.sqrt(E_rock_cal / rho_rock) * 1000
        statement_1 = "according to calculated Young's modulus"
        print(f"vE: {extensional_wave_velocity} (m/s; {statement_1})")
    else:
        print("Not enough information provided to calculate the E-wave velocity.")
        extensional_wave_velocity = 'nan'

    # Poisson's ratio
    if 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        # K_rock = kwargs.get('K_rock')
        # G_rock = kwargs.get('G_rock')
        poisson = (p_wave_velocity ** 2 - 2 * shear_wave_velocity ** 2) / (
                    2 * p_wave_velocity ** 2 - shear_wave_velocity ** 2)
        statement_1 = "according to bulk modulus, and shear modulus"
        print(f"v: {poisson} (-; {statement_1})")
    elif 'youngs_modulus_rock' in kwargs:
        poisson = (extensional_wave_velocity ** 2 - 2 * shear_wave_velocity ** 2) / (2 * shear_wave_velocity ** 2)
        statement_2 = "according to Young's modulus, and shear modulus"
        print(f"v: {poisson} (-; {statement_2})")
    # elif E_rock_cal is True:
    #     poisson = (extensional_wave_velocity ** 2 - 2 * shear_wave_velocity ** 2) / (2 * shear_wave_velocity ** 2)
    #     statement_3 = "according to shear modulus, and calculated Young's modulus"
    #     print(f"v: {poisson} (-; {statement_3})")
    else:
        print("Not enough information provided to calculate Poisson's ratio.")
        poisson = 'nan'

    return p_wave_velocity, shear_wave_velocity, extensional_wave_velocity, poisson


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
    # alpha-quartz
    bulk_modulus_rock = 37 * 1e-9
    shear_modulus_rock = 44 * 1e-9
    density = 2650
    vP, vS, vE, poisson = velocity(density, bulk_modulus_rock=bulk_modulus_rock, shear_modulus_rock=shear_modulus_rock)
