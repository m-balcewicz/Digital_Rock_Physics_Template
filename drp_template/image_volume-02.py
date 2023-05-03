from vtk.numpy_interface import dataset_adapter as dsa
from paraview.simple import *
from examples.data import load_100cube

data = load_100cube()

# Create a VTK dataset from the array
dataset = dsa.numpyTovtkDataArray(data.ravel(), 'Scalars')
dataset.SetDimensions(data.shape)
dataset.SetSpacing((1, 1, 1))

# Write the dataset to a VTK file
writer = vtk.vtkDataSetWriter()
writer.SetInputData(dataset)
writer.SetFileName('data.vtk')
writer.Write()

# Start ParaView and load the VTK file
paraview_cmd = 'pvpython'
paraview_script = 'load_data.py'
paraview_args = ['--script=' + paraview_script]
paraview_process = subprocess.Popen([paraview_cmd] + paraview_args)

# In the ParaView script, load the data and create a 3D visualization
with open(paraview_script, 'w') as f:
    f.write('from paraview.simple import *\n')
    f.write('reader = OpenDataFile("data.vtk")\n')
    f.write('Show(reader)\n')
    f.write('Render()\n')
    f.write('Interact()\n')

paraview_process.wait()