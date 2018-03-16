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
    """Class to hold a Terra Model read from fortran binary file."""

    def __init__(self, fn):
        self.filename = fn
        self._read_model()
        # self.get_cart()
        
    def _read_model(self):
        # open file for reading
        f = open(self.filename, 'rb')

        # initiate some BS values
        # x=y=r=vp=vs=rho=p=t=c=qp=qs=barycentres=triangles=cartpts = np.empty
  
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
        npts = np.fromfile(f, dtype='int32', count=1)[0]
        self.npts = npts
        skip(f)

        ## POPULATE LON ARRAY
        skip(f)
        self.lon = np.fromfile(f, dtype='float64', count=npts)
        skip(f)

        ## POPULATE LAT ARRAY
        skip(f)
        self.lat = np.fromfile(f, dtype='float64', count=npts)
        skip(f)

        ## GET NUMBER OF LAYERS
        skip(f)
        nlayers = np.fromfile(f, dtype='int32', count=1)[0]
        self.nlayers = nlayers
        skip(f)

        ## GET RADII ARRAY
        skip(f)
        self.r = np.fromfile(f, dtype='float64', count=nlayers)
        skip(f)

        ## NOW LOOP THROUGH AND READ DATA
        while True:

            # READ VARIABLE STRING
            skip(f)
            var_string = f.read(10).strip()
            skip(f)

            if var_string == b'VP':
                skip(f)
                self.vp = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'VS':
                skip(f)
                self.vs = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'RHO':
                skip(f)
                self.rho = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'P':
                skip(f)
                self.p = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'T':
                skip(f)
                self.t = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'C':
                skip(f)
                self.c = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'QP':
                skip(f)
                self.qp = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            elif var_string == b'QS':
                skip(f)
                self.qs = np.fromfile(f, dtype='float32', count=npts*nlayers).reshape(nlayers,npts)
                skip(f)
            else:
                # we're either done or something's wrong
                break

        # close_file  
        f.close()

    # Plotting
    ### note on plotting functions:
    #   due to the irregular lat/lon locations it is inefficient to use meshgrid
    #   hence it seems better to use the tri=True option of pcolor (which assumes
    #   an unstructured grid) than to use the "faster" pcolormesh.’

    def plot(self, *args, **kwargs):
        if 'vals' not in kwargs:
            raise Exception('vals must be specified, e.g., vals = self.vp')
        if 'radius' not in kwargs:
            default_radius = 3570
            kwargs['radius'] = default_radius
            print('radius defaulting to ' + str(default_radius))
        if 'projection' not in kwargs:
            default_projection = 'kav7'
            kwargs['projection'] = default_projection
        if 'lon_0' not in kwargs:
            kwargs['lon_0'] = 180
        if 'resolution' not in kwargs:
            kwargs['resolution'] = 'c'
        if 'cmap' not in kwargs:
            kwargs['cmap'] = 'RdYlBu'
        idx = find_nearest_index(self.r, kwargs['radius'])
        bmap = Basemap(projection=kwargs['projection'], lon_0=kwargs['lon_0'], resolution=kwargs['resolution'])
        x, y = bmap((self.lon+3600)%360, self.lat)
        bmap.pcolor(x, y, kwargs['vals'][idx], tri=True, cmap=kwargs['cmap'])
        bmap.drawcoastlines()
        bmap.colorbar()
        plt.show()
    
    # def plot_vs(self,radius=3570):
    #     idx = find_nearest_index(self.r, radius)
    #     map = Basemap(projection='mill',lon_0=180,resolution='c')
    #     x,y = map((self.lon+3600)%360,self.lat)
    #     map.pcolor(x,y,self.vs[idx],tri=True)
    #     map.drawcoastlines()
    #     map.colorbar()
    #     plt.show()
    



  
# def sph2cart(lat, lon, r):
#     lat = np.deg2rad(lat)
#     lon = np.deg2rad(lon)
#     z = r * np.sin(lat)
#     y = r * np.cos(lat) * np.sin(lon)
#     x = r * np.cos(lat) * np.cos(lon)
#     return x, y, z
#
#
# def get_cart(self):
#   self.x = self.y = self.z = np.zeros([self.r.size, self.lat.size])
#
#   for idx in np.arange(self.r.size):
#     self.x[idx,:], self.y[idx,:], self.z[idx,:] \
#     = sph2cart(self.lat,self.lon,self.r[idx]*np.ones(self.lat.size))
#
# function to find index of array nearest to a given value
# e.g. returns index of radius array closest to a given radius value
def find_nearest_index(array,value):
    return (np.abs(array-value)).argmin()

