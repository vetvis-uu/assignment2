from isosurface import *
import numpy
import vtk
import os

# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)

# Load volume dataset
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName('dragon.vtk')
reader.Update()
volume = reader.GetOutput()
dims = volume.GetDimensions()

# Extract surfels from volume
points = vtk.vtkPoints()
gradients = vtk.vtkFloatArray()
gradients.SetNumberOfComponents(3)
gradients.SetName("gradient")
for z in range(0, dims[2]-1):
    for y in range(0, dims[1]-1):
        for x in range(0, dims[0]-1):
            s = fetch_gridcell(x, y, z, volume)
            if min(s) < 127.5 and max(s) >= 127.5:
                pos, grad = compute_surfel(x, y, z, s)
                points.InsertNextPoint(pos[0], pos[1], pos[2])
                gradients.InsertNextTuple((grad[0], grad[1], grad[2]))

# Create cells for voxels
cells = vtk.vtkCellArray()
for index in range(points.GetNumberOfPoints()):
    cells.InsertNextCell(1, (index,))

# Create a vtkPolyData dataset from points and cells
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().AddArray(gradients)
polydata.SetVerts(cells)

# Write vtkPolyData dataset to file in VTK legacy format
writer = vtk.vtkPolyDataWriter()
writer.SetFileName('surfels.vtk')
writer.SetInputData(polydata)
writer.Write()
