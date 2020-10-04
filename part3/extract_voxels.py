from isosurface import *
import numpy
import vtk
import os

# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)

# Load volume
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName('dragon.vtk')
reader.Update()
volume = reader.GetOutput()
dims = volume.GetDimensions()

# Extract surface voxels from the volume
points = vtk.vtkPoints()
for z in range(1, dims[2]-1):
    for y in range(1, dims[1]-1):
        for x in range(1, dims[0]-1):
            value = volume.GetScalarComponentAsFloat(x, y, z, 0)
            if value > 127.5:
                s = fetch_voxel_neighbors(x, y, z, volume)
                if min(s) < 127.5:
                    points.InsertNextPoint(x, y, z)

# Create cells for surfels
cells = vtk.vtkCellArray()
for index in range(points.GetNumberOfPoints()):
    cells.InsertNextCell(1, (index,))

# Create a vtkPolyData dataset from points and cells
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(cells)

# Write vtkPolyData dataset to file in VTK legacy format
writer = vtk.vtkPolyDataWriter()
writer.SetFileName('voxels.vtk')
writer.SetInputData(polydata)
writer.Write()
