import numpy as np
import matplotlib.pyplot as plt
import porespy as ps
import openpnm as op
import imageio
import time
import multiprocessing
from logging  import new_log_entry

new_log_entry(f'DRP_snow: started')
filename_output = 'Output'

# Create workspace instance
ws = op.Workspace()

# Clear workspace 
ws.clear()
print(ws.keys())

# Create a project
project = ws.new project(name=filename_output)

# Read input
path = './Examples/Sandstone_1_12_800cube_TOTAL_POROSITY.raw'

# Load the binary data
with open(path, 'rb') as f:
    data = f.read()

# Convert the binary data to a 3D array
data = np.frombuffer(data, dtype='uint8').reshape((800, 800, 800))

# Read multiprocessing pool
#pool = multiprocessing.Pool()
#new_log_entry(pool)

# Calculate porosity
porosity = ps.metrics.porosity(data)
new_log_entry(f'porosity: {porosity}')

start = time.time()
#snow_output = ps.networks.snow2(phases=data, voxel_size=2.8e-6, parallelization={'cores': 24})
snow_output = ps.networks.snow2(phases=data, voxel_size=2.8e-6)
end = time.time()

# Create empty dummy network
#pn = op.network.GenericNetwork(project=project)

# Update openpnm pore network
#pn.update(snow_output)

new_log_entry(f'DRP_snow took: {end-start} second(s)')

pn = op.io.network_from_porespy(snow_putput.network)
#new_log_entry(pn)
imageio.volsave('./Sandstone_1_12.tif', np.array(data, dtype=np.int8))
op.io.project_to_vtk(project=pn.project)

# Save project
ws.save_project(project, filename=filename_output)
ws.close_project(project)
new_log_entry('DRP_snow: finished')
