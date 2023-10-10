# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Elastic Moduli: Isotropic Form of Hooke’s Law
# The bulk modulus, K, is defined as the ratio of the hydrostatic stress, σ0, to the volumetric strain:
# according to Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook.
# Cambridge University Press (2020)
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
    print('Welcome Elastic Moduli calculations linear and elastic media')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to ')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def elastic_moduli(**kwargs):
    if 'c_11' in kwargs and 'c_44' in kwargs:
        if 'density' in kwargs:
            density = kwargs.get('density')
            c_11 = kwargs.get('c_11')
            c_44 = kwargs.get('c_44')
            p_wave_velocity = math.sqrt(c_11 / density)
            shear_wave_velocity = math.sqrt(c_44 / density)
            # print(f"vP: {p_wave_velocity} (m/s)")
            # print(f"vS: {shear_wave_velocity} (m/s)")

            return p_wave_velocity, shear_wave_velocity

        else:
            c_11 = kwargs.get('c_11')
            c_44 = kwargs.get('c_44')
            bulk_modulus = c_11 - 4 / 3 * c_44
            shear_modulus = c_44
            # statement_1 = "according to bulk modulus, and shear modulus"
            # print(f"bulk modulus: {bulk_modulus} (Pa)")
            # print(f"shear modulus: {shear_modulus} (Pa)")

            return bulk_modulus, shear_modulus

    elif 'bulk_modulus_mineral' in kwargs and 'shear_modulus_mineral' in kwargs:
        bulk_modulus_mineral = kwargs.get('bulk_modulus_mineral')
        shear_modulus_mineral = kwargs.get('shear_modulus_mineral')
        c_44 = shear_modulus_mineral
        c_11 = bulk_modulus_mineral + 4 / 3 * shear_modulus_mineral
        # statement_1 = "according to bulk modulus, and shear modulus"
        # print(f"c_11_cement: {c_11} (Pa)")
        # print(f"c_44_cement: {c_44} (Pa)")

        return c_11, c_44

    elif 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        bulk_modulus_rock = kwargs.get('bulk_modulus_rock')
        shear_modulus_rock = kwargs.get('shear_modulus_rock')

        youngs_modulus_rock = (9 * bulk_modulus_rock * shear_modulus_rock)/(3 * bulk_modulus_rock + shear_modulus_rock)

        return youngs_modulus_rock

    elif 'density' in kwargs and 'p_wave_velocity' in kwargs and 'shear_wave_velocity' in kwargs:
        density = kwargs.get('density')
        p_wave_velocity = kwargs.get('p_wave_velocity')
        shear_wave_velocity = kwargs.get('shear_wave_velocity')
        c_11 = p_wave_velocity * p_wave_velocity * density
        c_44 = shear_wave_velocity * shear_wave_velocity * density
        # statement_1 = "according to P-wave velocity, and S-wave velocity for isotropic symmetry"
        # print(statement_1)
        # print(f"c_11_cement: {c_11} (Pa)")
        # print(f"c_44_cement: {c_44} (Pa)")

        return c_11, c_44

    elif 'youngs_modulus_mineral' in kwargs and 'poisson_mineral' in kwargs:
        youngs_modulus_mineral = kwargs.get('youngs_modulus_mineral')
        poisson_mineral = kwargs.get('poisson_mineral')
        c_11 = (youngs_modulus_mineral * (1 - poisson_mineral)) / ((1 + poisson_mineral) * (1 - 2 * poisson_mineral))
        c_44 = youngs_modulus_mineral / (2 + 2 * poisson_mineral)

        return c_11, c_44

    # elif 'youngs_modulus_rock' in kwargs and 'poisson_rock' in kwargs:
    #     youngs_modulus_rock = kwargs.get('youngs_modulus_rock')
    #     poisson_rock = kwargs.get('poisson_rock')
    #     bulk_modulus_rock = youngs_modulus_rock / (3 * (1 - 2 * poisson_rock)
    #     shear_modulus_rock = youngs_modulus_rock / (2 + 2 * poisson_rock)
    #
    #     return bulk_modulus_rock, shear_modulus_rock

    else:
        print("Not enough information provided to calculate the elastic moduli")
        bulk_modulus = 'nan'
        shear_modulus = 'nan'
        c_11 = 'nan'
        c_44 = 'nan'


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
    # K_quartz, G_quartz = ElasticModuli(c_11_cement=68, c_44_cement=33.5)
    # K_quartz, G_quartz = elastic_moduli(c_11=68e9, c_44=33.5e9)
    K_quartz, G_quartz = elastic_moduli(c_11=86.6e9, c_44=57.8e9)
    p_wave_quartz, s_wave_quartz = elastic_moduli(density=2650, c_11=68e9, c_44=33.5e9)
    # according to Balcewicz 2021
    print(f'elastic constants according to Balcewicz 2021')
    print(f'K-QUARTZ: {K_quartz * 1e-9} (GPa)')
    print(f'G-QUARTZ: {G_quartz * 1e-9} (GPa)')
    print(f'P-wave velocity QUARTZ: {p_wave_quartz} (m/s)')
    print(f'S-wave velocity QUARTZ: {s_wave_quartz} (m/s)')

    #  according to Andrä 2013b
    c11_quartz, c44_quartz = elastic_moduli(bulk_modulus_mineral=37.0e9, shear_modulus_mineral=44.0e9)
    print(f'elastic constants according to Andrä 2013')
    print(f'c11-QUARTZ: {c11_quartz * 1e-9} (GPa)')
    print(f'c44-QUARTZ: {c44_quartz * 1e-9} (GPa)')
    c11_calcite, c44_calcite = elastic_moduli(bulk_modulus_mineral=68.3e9, shear_modulus_mineral=28.4e9)
    print(f'c11-CALCITE: {c11_calcite * 1e-9} (GPa)')
    print(f'c44-CALCITE: {c44_calcite * 1e-9} (GPa)')
    c11_dolomite, c44_dolomite = elastic_moduli(bulk_modulus_mineral=94.9e9, shear_modulus_mineral=45.0e9)
    print(f'c11-DOLOMITE: {c11_dolomite * 1e-9} (GPa)')
    print(f'c44-DOLOMITE: {c44_dolomite * 1e-9} (GPa)')

    c11_quartz, c44_quartz = elastic_moduli(density=2650, p_wave_velocity=6050, shear_wave_velocity=4090)
    print(f'elastic constants according to Andrä 2013')
    print(f'c11-QUARTZ: {c11_quartz * 1e-9} (GPa)')
    print(f'c44-QUARTZ: {c44_quartz * 1e-9} (GPa)')

    p_wave_quartz, s_wave_quartz = elastic_moduli(density=2650, c_11=95.56e9, c_44=44.0e9)
    print(f'P-wave velocity QUARTZ: {p_wave_quartz} (m/s)')
    print(f'S-wave velocity QUARTZ: {s_wave_quartz} (m/s)')
    # density = 2650, c_11_cement = 96.99e9, c_44_cement = 44.32e9
    # vP: 6049.79338490167 (m/s)
    # vS: 4089.5633387791895 (m/s)
    # density = 2650, c_11_cement = 95.56e9, c_44_cement = 44.0e9
    # vP: 6005.029338686912 (m/s)
    # vS: 4074.7728261714983 (m/s)
