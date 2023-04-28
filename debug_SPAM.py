import matplotlib.pyplot as plt
import spam.deformation
import spam.DIC
import spam.datasets

# Load data_normal
snow = spam.datasets.loadSnow()

# Define transformation to apply
transformation = {'t': [0.0, 3.0, 2.5],
                   'r': [5.0, 0.0, 0.0]}

# Convert this into a deformation function
Phi = spam.deformation.computePhi(transformation)

# Apply this to snow data_normal
snowDeformed = spam.DIC.applyPhi(snow, Phi=Phi)

# Show the difference between the initial and the deformed image.
# Here we used the blue-white-red colourmap "coolwarm"
# which makes 0 white on the condition of the colourmap being symmetric around zero,
# so we force the values with vmin and vmax.
plt.figure()
plt.imshow((snow - snowDeformed)[50], cmap='coolwarm', vmin=-36000, vmax=36000)
plt.savefig('spam-figure.png', format='png')
