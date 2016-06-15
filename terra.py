#!/usr/bin/env

# import argparse
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

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
    elif ( var_string == 'BARYCENTRE' ):
      skip(f)
      barycentres = np.fromfile(f, dtype='float64', count=npts*nlayers).reshape(npts*3,nlayers)
      skip(f)
    elif ( var_string == 'TRIANGLES' ):
      skip(f)
      triangles = np.fromfile(f, dtype='int32', count=npts*nlayers).reshape(npts*3,nlayers)
      skip(f)
    elif ( var_string == 'CART_POINT' ):
      skip(f)
      cartpts = np.fromfile(f, dtype='float64', count=npts*nlayers).reshape(npts*3,nlayers)
      skip(f)
    else:
      # we're either done or something's wrong
      break

  # close_file  
  f.close()
  
  return x,y,r,vp,vs,rho,p,t,c,qp,qs,barycentres,triangles,cartpts


def plot_slice(m,r):
  ax = plt.axes(projection=ccrs.PlateCarree())
  ax.coastlines()
  ax.imshow



#   
# # Define the model class
# class terra_model:
# 
#   # Read model from fortran binary
#   def readfort(self,file):
#   
