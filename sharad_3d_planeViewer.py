#!/usr/local/bin/python3
# Example SHARAD 3D array plane viewer

# Libraries
import numpy as np
import matplotlib.pyplot as plt
import sys

def parseargs():
    #
    # Default Values
    #
    # Input file
    #
    radar_volume_path = './PLANUM_BOREUM_3D_TIME.DAT'

  return radar_volume_path, 

def readdata(radar_volume_path, radar_volume_size):
  #
  # Read in the data volume
  #
  dc = np.fromfile(radar_volume_path, dtype='<f', count=-1)
  #
  # Reshape to datacube
  #
  dc = np.reshape(datacube, radar_volume_size).transpose()   
  rvs_X = radar_volume_size[2]
  rvs_Y = radar_volume_size[1]
  rvs_Z = radar_volume_size[0]
  return dc, rvs_X, rvs_Y, rvs_Z 
  
def main():
  #
  # Parse command line arguments and set default values
  #
  radar_volume_path = parseargs()
  #
  # Read in the data volume
  #
  datacube, radar_volume_size_X, radar_volume_size_Y, radar_volume_size_Z = 
    readdata(radar_volume_path, radar_volume_size)
  # ----------- enter parameters here ----------------
  # Information about the input file
  radar_volume_path = '/Users/mperry/OneDrive/Documents/Work/PSI/Projects/3D_Challenge/PLANUM_BOREUM_3D_TIME.DAT'
  # Properties for each exis in [x,y,z] form
#  radar_volume_size = [300,300,937]
  radar_volume_size = [937,300,300] #Python workaround; put z dimension first
  axis_unit = ['m','m','us']
  axis_start = [189762,-498988,107.400];
  axis_interval = [475, 475, 0.0375]
  
  # information to map pixels in the file to coordinates (these names are the
  # same as those used in the label)
  line_first_pixel = 3101;
  sample_first_pixel = 1651;

  # specify the plane, in coordinate space
  X_value = 3101;
  Y_value = 'all';
  Z_value = 'all';

  # ----------- end parameters -----------------------

  datacube = np.fromfile(radar_volume_path, dtype='<f', count=-1)
  datacube = np.reshape(datacube, radar_volume_size).transpose()

  radar_volume_size_X = radar_volume_size[2]
  radar_volume_size_Y = radar_volume_size[1]
  radar_volume_size_Z = radar_volume_size[0]

  # Z (time) always has indices indexed from zero
  band_first_pixel = 0;

  if X_value == 'all':
    X_value = np.arange(line_first_pixel, line_first_pixel + radar_volume_size_X)
  if Y_value == 'all':
    Y_value = np.arange(sample_first_pixel, sample_first_pixel + radar_volume_size_Y)
  if Z_value == 'all':
    Z_value = np.arange(band_first_pixel, band_first_pixel + radar_volume_size_Z)
  
  # translate to pixel space indices
  X_value_filecoords = X_value - line_first_pixel
  Y_value_filecoords = Y_value - sample_first_pixel
  Z_value_filecoords = Z_value - band_first_pixel 
  #
  # Put a more advance log print out here
  #
  if type(X_value_filecoords) is not int:
    print(len(X_value_filecoords))
  if type(Y_value_filecoords) is not int:
    print(len(Y_value_filecoords))
  if type(Z_value_filecoords) is not int:
    print(len(Z_value_filecoords))

  if np.any(X_value_filecoords < 0) or np.any(X_value_filecoords >= radar_volume_size_X):
    print('Specified X_value is out of bounds for this image')
    return
  if np.any(Y_value_filecoords < 0) or np.any(Y_value_filecoords >= radar_volume_size_Y): 
    print('Specified Y_value is out of bounds for this image')
    return
  if np.any(Z_value_filecoords < 0) or np.any(Z_value_filecoords >= radar_volume_size_Z):
    print('Specified Z_value is out of bounds for this image')
    return
  
  # The transpose ensures that the first non-singleton dimension in the
  # squeezed matrix (in alpha order) will be interpreted as different
  # columns/x-values
  if type(X_value) is int:
    plane = np.squeeze(datacube[X_value_filecoords, Y_value_filecoords[0]:, Z_value_filecoords[0]:])
  elif type(Y_value) is int:
    plane = np.squeeze(datacube[X_value_filecoords[0]:, Y_value_filecoords, Z_value_filecoords[0]:])
  elif type(Z_value) is int:
    plane = np.squeeze(datacube[X_value_filecoords[0]:, Y_value_filecoords[0]:, Z_value_filecoords])
  plane = np.transpose(plane)
  
  # Go through the dimensions checking sizes to get the labeling right

#  dim_values_coords = np.array([X_value,Y_value,Z_value])
#  dim_values_filecoords = np.array([X_value_filecoords,Y_value_filecoords,Z_value_filecoords])
#  dim_names = ['X','Y','Z']

#  horiz_dim_name = ''
#  vert_dim_name = ''
#  sliced_dim_name = ''

#  for d in range(3):
#    if np.shape(dim_values_coords[d]) == () and sliced_dim_name == '': # the first singleton dimension gets the honor of naming the image 
#      sliced_dim_name = dim_names[d]
#      sliced_dim_coordinate = dim_values_coords[d] 
#    else:
#      if horiz_dim_name == '': # %  horizontal dim yet
#        hor_dim_name = '{} ({})'.format(dim_names[d],axis_unit[d]);

        # Calculate lower & upper bounds in the units of the image's
        # underlying coordinates, which we can get from zero-indexed
#        horiz_dim_lower = axis_start[d] + axis_interval[d]*(np.min(dim_values_filecoords[d]))
#        horiz_dim_upper = axis_start[d] + axis_interval[d]*(np.max(dim_values_filecoords[d]))
#      elif vert_dim_name == '':
#        vert_dim_name = '{} ({})'.format(dim_names[d],axis_unit[d])
        
        # Calculate lower & upper bounds in the units of the image's
        # underlying coordinates, which we can get from zero-indexed
#        vert_dim_lower = axis_start[d] + axis_interval[d]*(np.min(dim_values_filecoordsr[d]));
#        vert_dim_upper = axis_start[d] + axis_interval[d]*(np.max(dim_values_filecoords[d]))
#      else:
#        print('At least one dimension must have only one value specified in order to plot as a plane')
#        return
  #
  # Plotting
  #
  base_name = 'test'
  p = plt.imshow(plane, cmap='gray')
  plt.show()
  return

if __name__ == '__main__':
  main()
