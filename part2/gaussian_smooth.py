import vtk
import os

# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName('ctscan_ez_bin.vtk')

gs = vtk.vtkImageGaussianSmooth()
gs.SetInputConnection(reader.GetOutputPort())
gs.SetStandardDeviation(1.0)  # Filter radius = (sigma * 3)

writer = vtk.vtkStructuredPointsWriter()
writer.SetFileName('ctscan_ez_smooth.vtk')
writer.SetInputConnection(gs.GetOutputPort())
writer.Update()
