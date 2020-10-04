import numpy
import vtk


def fetch_voxel_neighbors(x, y, z, vtk_volume):
    """ Fetch scalar values of voxels in 6-connected neighborhod """
    s = (vtk_volume.GetScalarComponentAsFloat(x-1, y, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x+1, y, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y-1, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y+1, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y, z-1, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y, z+1, 0))
    return s


def fetch_gridcell(x, y, z, vtk_volume):
    """ Fetch corners (eight scalar values) of grid cell in volume """
    s = (vtk_volume.GetScalarComponentAsFloat(x, y, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x+1, y, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y+1, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x+1, y+1, z, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y, z+1, 0),
        vtk_volume.GetScalarComponentAsFloat(x+1, y, z+1, 0),
        vtk_volume.GetScalarComponentAsFloat(x, y+1, z+1, 0),
        vtk_volume.GetScalarComponentAsFloat(x+1, y+1, z+1, 0))
    return s


def compute_surfel(x, y, z, s):
    """ Compute surfel from grid cell location and scalars.
        
    This function assumes that scalars s are in range [0,255] and
    represent coverage values.
    """
    coverage = sum(s) / 8.0
    signed_dist_approx = (0.5 - (coverage / 255.0)) * 1.4
    grad_x = (s[1] + s[3] + s[5] + s[7]) - (s[0] + s[2] + s[4] + s[6])
    grad_y = (s[2] + s[3] + s[6] + s[7]) - (s[0] + s[1] + s[4] + s[5])
    grad_z = (s[4] + s[5] + s[6] + s[7]) - (s[0] + s[1] + s[2] + s[3])
    grad_mag = max(1e-5, (grad_x*grad_x + grad_y*grad_y + grad_z*grad_z)**0.5)
    pos_x = x + signed_dist_approx * (grad_x / grad_mag)
    pos_y = y + signed_dist_approx * (grad_y / grad_mag)
    pos_z = z + signed_dist_approx * (grad_z / grad_mag)
    return (pos_x, pos_y, pos_z), (grad_x, grad_y, grad_z)