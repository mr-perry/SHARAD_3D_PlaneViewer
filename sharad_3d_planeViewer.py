#!/usr/local/bin/python3
# Example SHARAD 3D array plane viewer

# Libraries
import argparse, sys, os
import numpy as np
import matplotlib.pyplot as plt

def parseargs(prog, vers):
  #
  # Default Values
  #
  err = 0				# Error flag
  rvs = [937,300,300]			# Radar volume size
  rvp = './PLANUM_BOREUM_3D_TIME.DAT'   # Radar volume path
  au = ['m','m','us']			# Axis units
  ast = [189762,-498988,107.400];	# Axis start values
  ai = [475, 475, 0.0375]		# Axis Intervals
  #
  # Information to map pixels in the file to coordinates (these names are the
  # same as those used in the label)
  # -- CONVERT TO READ LABEL FILE
  #
  lfp = 3101;				# Line first pixel
  sfp = 1651;				# Sample first pixel
  bfp = 0;				# Band first pixel
  #
  # specify the plane, in coordinate space
  # 
  xv = 'all';				# Default X value
  yv = 'all';				# Default Y value
  zv = 'all';				# Default Z value
  #
  # Initiate parser
  #
  parser = argparse.ArgumentParser(description=str(prog + ' ' + str(vers)))
  #
  # Optional Arguments
  #
  parser.add_argument('-rvp', nargs=1, default=rvp, type=str,
		help="Path to the radar volume")
  parser.add_argument('-xv', nargs=1, default=xv, 
		help="X-value slice. Integer or all")
  parser.add_argument('-yv', nargs=1, default=yv,
		help="Y-value slice. Integer or all")
  parser.add_argument('-zv', nargs=1, default=zv,
		help="Z-value slice. Integer or all")
  #
  # Parse Arguments
  #
  args = parser.parse_args()
  if args.xv != xv:
    xv = int(args.xv[0])
    if xv < lfp:
      err = "X-Value must be greater than or equal to {}".format(str(lfp)) 
  if args.yv != yv:
    yv = int(args.yv[0])
    if yv < sfp:
      err = "Y-Value must be greater than or equal to {}".format(str(sfp)) 
  if args.zv != zv:
    zv = int(args.zv[0])
    if zv < bfp:
      err = "Y-Value must be greater than or equal to {}".format(str(bfp)) 
  if args.rvp != rvp:
    rvp = str(args.rvp[0])
  #
  # Error check
  #
  if (type(xv) is int and type(yv) is int) or (type(xv) is int and type(zv) is int) or (type(yv) is int and type(zv) is int):
    err = 'ERROR: Only one dimension can be an integer. The other two must be "all".'
  if (type(xv) is str and type(yv) is str and type(zv) is str):
    err = 'ERROR: You must specify a singleton dimension'
  if not os.path.isfile(rvp):
    err = 'ERROR: Radar volume not found. Please check your path.'
  #
  # Print log results
  #
  print('----------------------------')
  print('Radar Volume Size:\t{}'.format(rvs))
  print('Radar Volume Path:\t{}'.format(rvp))
  print('----- Plane Dimensions -----')
  print('X-Values:\t{}'.format(str(xv)))
  print('Y-Values:\t{}'.format(str(yv)))
  print('Z-Values:\t{}'.format(str(zv)))
  print('----------------------------')
  return rvs, rvp, au, ast, ai, lfp, sfp, bfp, xv, yv, zv, err

def readdata(radar_volume_path, radar_volume_size):
  #
  # Read in the data volume
  #
  dc = np.fromfile(radar_volume_path, dtype='<f', count=-1)
  #
  # Reshape to datacube
  #
  dc = np.reshape(dc, radar_volume_size).transpose()   
  rvs_X = radar_volume_size[2]
  rvs_Y = radar_volume_size[1]
  rvs_Z = radar_volume_size[0]
  return dc, rvs_X, rvs_Y, rvs_Z 
  
def main():
  prog = "SHARAD 3D Plane Viewer"
  vers = "1.0"
  #
  # Parse command line arguments and set default values
  #
  [radar_volume_size, radar_volume_path, axis_unit, 
    axis_start, axis_interval, line_first_pixel, sample_first_pixel,
    band_first_pixel, x_value, y_value, z_value, err] = parseargs(prog, vers)
  if err != 0:
    print(err)
    return
  else:
    #
    # Read in the data volume
    #
    [datacube, radar_volume_size_X, radar_volume_size_Y, \
      radar_volume_size_Z] = readdata(radar_volume_path, radar_volume_size)

    # Z (time) always has indices indexed from zero

    if x_value == 'all':
      x_value = np.arange(line_first_pixel, line_first_pixel + radar_volume_size_X)
    if y_value == 'all':
      y_value = np.arange(sample_first_pixel, sample_first_pixel + radar_volume_size_Y)
    if z_value == 'all':
      z_value = np.arange(band_first_pixel, band_first_pixel + radar_volume_size_Z)
  
  # translate to pixel space indices
  X_value_filecoords = x_value - line_first_pixel
  Y_value_filecoords = y_value - sample_first_pixel
  Z_value_filecoords = z_value - band_first_pixel 
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
  if type(x_value) is int:
    plane = np.squeeze(datacube[X_value_filecoords, Y_value_filecoords[0]:, Z_value_filecoords[0]:])
  elif type(y_value) is int:
    plane = np.squeeze(datacube[X_value_filecoords[0]:, Y_value_filecoords, Z_value_filecoords[0]:])
  elif type(z_value) is int:
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
