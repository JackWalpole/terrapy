#!/usr/bin/env

# import argparse
import numpy

# parser = argparse.ArgumentParser(description="Read terra model to numpy array")
# parser.add_argument("File", help="Name of terra model file in fortran binary format")
# 
# call

# Define function to read terra file to numpy array
# Sanity checks are not built-in yet so take care to check
# the files are read in sensibly!

def read_terra_to_model(fn):

  # open file for reading
  f = open(fn,'rb')
  
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
  
  ## NOW LOOP THROUGH UNTIL END OF FILE
  while True:
    # READ VARIABLE STRING
    skip(f)
    var_string = f.read(10)
    skip(f)
    
    
  
  return x,y

     


#   
# # Define the model class
# class terra_model:
# 
#   # Read model from fortran binary
#   def readfort(self,file):
#   
