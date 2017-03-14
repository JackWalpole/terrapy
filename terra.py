#!/usr/bin/env

# 
# # for SHTOOLS
# import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages')
# import pyshtools as shtools

import numpy as np
# import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import scipy.stats as stats

# from scipy.interpolate import LSQSphereBivariateSpline

class TerraMod:

  def __init__(self,fn):
    self.filename = fn
    self.lon, self.lat, self.r, \
    self.vp, self.vs, self.rho, \
    self.p, self.t, self.c, \
    self.qp, self.qs, \
    self.barycentres, \
    self.triangles, \
    self.cartpts = read_model(fn)
    get_cart(self)

### note on plotting functions:
#   due to the irregular lat/lon locations it is inefficient to use meshgrid
#   hence it seems better to use the tri=True option of pcolor (which assumes
#   an unstructured grid) than to use the "faster" pcolormesh.

  def plot_vp(self,radius=3570):
    idx = find_nearest_index(self.r,radius)
    map = Basemap(projection='kav7',lon_0=180,resolution='c')
    x,y = map((self.lon+3600)%360,self.lat)
    map.pcolor(x,y,self.vp[idx],tri=True,cmap='RdYlBu')
    map.drawcoastlines()
    map.colorbar()
    plt.show()
    
  def plot_vs(self,radius=3570):
    idx = find_nearest_index(self.r,radius)
    map = Basemap(projection='mill',lon_0=180,resolution='c')
    x,y = map((self.lon+3600)%360,self.lat)
    map.pcolor(x,y,self.vs[idx],tri=True)
    map.drawcoastlines()
    map.colorbar()
    plt.show()
    

      
#     self.x, self.y, self.z = np.zeros([self.r.size, self.lat.size])
    
#     self.x, self.y, self.z = sph2cart(self.lat,self.lon,self.r)
    
#   def plot_vs(self):
#     map = Basemap(projection='mill',lon_0=180,resolution='c')
#     x,y = map((self.lon+3600)%360,self.lat)
#     map.pcolor(x,y,self.vs[0],tri=True)
#     map.drawcoastlines()
#     plt.show()

#   def plot_vs_smooth(self):
#     map = Basemap(projection='mill',lon_0=180)
#     # get spherical harmonic coefficients
#     cilm, chi2 = shtools.SHExpandLSQ(self.vs[0],self.lat,self.lon,50)
#     grid = shtools.MakeGrid2D(cilm,50)
#     nx = grid.shape[1]
#     ny = grid.shape[0]
#     lons, lats = map.makegrid(nx,ny)
#     x, y = map(lons,lats)
#     map.contourf(x,y,grid)
#     map.drawcoastlines()
#     plt.show()
    
#     lons = np.linspace(-180,179,360)
#     lats = np.linspace(-90,90,181)
    
    
    
# def SH(vp):
#   cilm, chi2 = shtools.SHExpandLSQ(d,lat,lon,lmax
  
#   
#     # sort lon lat
#     ind = np.lexsort((self.lat,self.lon))
#     d = np.array([[self.lon[i],self.lat[i],self.vp[r][i]] for i in ind])
    
    
#     ax = plt.axes(projection=ccrs.PlateCarree())
# #     ax.coastlines()
#     plt.pcolormesh(self.lon,self.lat,self.vp[r,:])
#     plt.show()
#     return ax
    


# def xyz2grid(x,y,z):
#   # takes 3 1d numpy arrays of equal size
#   # and outputs to mesh for plotting
#   
#   # first identify unique nodes
#   xu = np.unique(x)
#   yu = np.unique(y)
#   
#   # grid these
#   X, Y = np.meshgrid(xu,yu)
#   
#   # now index
#   xi = np.searchsorted(xu,x)
#   yi = np.searchsorted(yu,y)
#   
#   # now setup and populate Z
#   Z = np.zeros([xu.size,yu.size])
#   for ii in np.arange(z.size):
#     Z[xi[ii],yi[ii]] = z[ii]
# 
#   # return the meshgrid and values X,Y,Z
#   return X,Y,Z
  
  
def read_model(fn):

  # open file for reading
  f = open(fn,'rb')
  
  # initiate some BS values
  x=y=r=vp=vs=rho=p=t=c=qp=qs=barycentres=triangles=cartpts = np.empty
  
  # USEFUL FUNCTION 
  def skip(f):
    # function to skip past the 4 byte chunks
    # at the start and end of records in the
    # unformatted fortran files 
    # (these bytes code an integer telling
    # how many bytes are in the record)
    nb = np.fromfile(f, dtype='int32', count=1)

  ##############################
  # Begin interrogating the file
  ##############################
  
  ## GET VERSION STRING
  skip(f)
  version_string = f.read(30)
  skip(f)
  
  # GET NUMBER OF POINTS
  skip(f)
  npts = np.fromfile(f, dtype='int32', count=1)
  skip(f)
  
  ## POPULATE X ARRAY
  skip(f)
  x = np.fromfile(f, dtype='float64', count=npts)
  skip(f)
  
  ## POPULATE Y ARRAY
  skip(f)
  y = np.fromfile(f, dtype='float64', count=npts)
  skip(f)
  
  ## GET NUMBER OF LAYERS
  skip(f)
  nlayers = np.fromfile(f, dtype='int32', count=1)
  skip(f)
  
  ## GET RADII ARRAY
  skip(f)
  r = np.fromfile(f, dtype='float64', count=nlayers)
  skip(f)
  
  ## NOW LOOP THROUGH AND READ DATA
  while True:
  
    # READ VARIABLE STRING
    skip(f)
    var_string = f.read(10).strip()
#     print 'reading:', var_string
    skip(f)
    
    if ( var_string == 'VP' ):
      skip(f)
      vp = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'VS' ):
      skip(f)
      vs = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'RHO' ):
      skip(f)
      rho = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'P' ):
      skip(f)
      p = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'T' ):
      skip(f)
      t = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'C' ):
      skip(f)
      c = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'QP' ):
      skip(f)
      qp = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
    elif ( var_string == 'QS' ):
      skip(f)
      qs = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
      skip(f)
#     elif ( var_string == 'BARYCENTRE' ):
#       skip(f)
#       barycentres = np.fromfile(f, dtype='float64', count=npts*nlayers).reshape(npts*3,nlayers)
#       skip(f)
#     elif ( var_string == 'TRIANGLES' ):
#       skip(f)
#       triangles = np.fromfile(f, dtype='int32', count=npts*nlayers).reshape(npts*3,nlayers)
#       skip(f)
#     elif ( var_string == 'CART_POINT' ):
#       skip(f)
#       cartpts = np.fromfile(f, dtype='float64', count=npts*nlayers).reshape(npts*3,nlayers)
#       skip(f)
    else:
      # we're either done or something's wrong
      break

  # close_file  
  f.close()
  
  return x,y,r,vp,vs,rho,p,t,c,qp,qs,barycentres,triangles,cartpts

def get_cart(self):
  self.x = self.y = self.z = np.zeros([self.r.size, self.lat.size])
  def sph2cart(lat,lon,r):
	lat = np.deg2rad(lat)
	lon = np.deg2rad(lon)
	z = r * np.sin(lat)
	y = r * np.cos(lat) * np.sin(lon)
	x = r * np.cos(lat) * np.cos(lon)
	return x,y,z
  for idx in np.arange(self.r.size):
	self.x[idx,:], self.y[idx,:], self.z[idx,:] \
	= sph2cart(self.lat,self.lon,self.r[idx]*np.ones(self.lat.size))

# function to find index of array nearest to a given value
# e.g. returns index of radius array closest to a given radius value
def find_nearest_index(array,value):
    return (np.abs(array-value)).argmin()

