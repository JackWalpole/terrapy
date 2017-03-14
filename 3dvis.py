#!/usr/bin/env python

import numpy as np
import terra as t

# import mlab from mayavi for 3D visualisation
from mayavi import mlab
from mayavi.sources.builtin_surface import BuiltinSurface

# Earth radius (km)
r=6370.
cmb=3480.

def plot_earth():
	###############################################################################
	# Display continents outline, using the VTK Builtin surface 'Earth'

# 	continents_src = BuiltinSurface(source='earth', name='Continents')
# 	# The on_ratio of the Earth source controls the level of detail of the 
# 	# continents outline.
# 	continents_src.data_source.on_ratio = 2
# 	continents_src.data_source.radius = r
# 	continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0))

	###############################################################################
	# Display a semi-transparent sphere, for the 410 km disc.

	# We use a sphere Glyph, throught the points3d mlab function, rather than
	# building the mesh ourselves, because it gives a better transparent
	# rendering.
	r410 = r - 410
	r660 = r - 660
	r2591 = r - 2591
	r2891 = r - 2891
	r5150 = r - 5150
	sphere0 = mlab.points3d(0, 0, 0, scale_mode='none',
									scale_factor=r*2,
									color=(0., 0., 0.),
									resolution=50,
									opacity=0.1,
									name='Earth')
									
def plot_slice_vp(model):
  x = model.x[1,:]
  y = model.y[1,:]
  z = model.z[1,:]
  s = model.vp[1,:]
  mesh = mlab.mesh(x,y,z,scalars=s,opacity=1,colormap="jet")						

def interp_to_grid(model,layer):
  from scipy.interpolate import SmoothSphereBivariateSpline
  theta = np.deg2rad(90-model.lat)
  phi = np.deg2rad(model.lon)
  r = model.vp[layer,:]
  lut = SmoothSphereBivariateSpline(theta,phi,r)
  return lut
  
  phi, theta = np.mgrid[0:np.pi:101j,0:2*np.pi:101j]
  gx = r * np.sin(phi) * np.cos(theta)
  gy = r * np.sin(phi) * np.sin(theta)
  gz = r * np.cos(phi)
  return griddata((x[r,:],y[r,:],z[r,:]),A.vp[r],(gx,gy,gz),method='cubic')


# read in the model
A = t.TerraMod('../TERRAFiles/gmt700.001.tess.all_vars.lev6.fort')



# PLOT STUFF
mlab.clf()
plot_earth()
plot_slice_vp(A)

