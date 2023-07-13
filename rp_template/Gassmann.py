# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Gassmann’s Relations: Isotropic Form
# according to Gassmann’s relations for Isotropic Form by Mavko, G., Mukerji, T.,
# Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)
#
# by Martin Balcewicz martin.balcewicz@rockphysics.org 01/2023

# One of the most important problems in the rock physics analysis of logs, cores, and seismic data is using seismic
# velocities in rocks saturated with one fluid to predict those of rocks saturated with a second fluid,
# or equivalently, predicting saturated-rock velocities from dry-rock velocities, and vice versa. This is the seismic
# fluid substitution problem. Gassmann works best for very low-frequency in-situ seismic data (<100 Hz) and may
# perform less well as frequencies increase toward sonic logging ð≈104 HzÞ and laboratory ultrasonic measurements
# ð≈106 HzÞ.
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to Gassmann\'s relations for Isotropic Form calculations')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print(' ')
    print('Applied equations according to # Gassmann\'s Relations: Isotropic Form by')
    print('Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook. Cambridge University Press (2020)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')

def gassmann(phase, porosity, K_fluid_1, K_fluid_2, K_sat_1, K_sat_2):


    Gassmann_K_sat = 1

    return Gassmann_K_sat


# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# Example-1
# phase = ['Quartz', 'Water']
# bulk_modulus_rock = 12e-9
# bulk_modulus_mineral = 36e-9
# shear_modulus_rock_dry =
# shear_modulus_rock_wet =
# fraction = (0.6, 0.4)
# density = (2650, 1000)  # kg/m^3
# porosity = 0.2
# K_sat_1 = bulk_modulus_[0]
# K_sat_2 = bulk_modulus[1]
# K_fluid_1 = 1
# K_fluid_2 = 2

Gassmann_K_sat = gassmann(phase, porosity, K_fluid_1, K_fluid_2, K_sat_1, K_sat_2)

if __name__ == '__main__':
    main()
    print(f'{Gassmann_K_sat}')
