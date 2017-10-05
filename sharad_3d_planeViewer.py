#!/usr/local/bin/python3
# Example SHARAD 3D array plane viewer

# Libraries
import argparse, sys, os
from os.path import basename
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
  ast = [189762,-498988,107.400]	# Axis start values
  ai = [475, 475, 0.0375]		# Axis Intervals
  #
  # Information to map pixels in the file to coordinates (these names are the
  # same as those used in the label)
  # -- CONVERT TO READ LABEL FILE
  #
  lfp = 3101				# Line first pixel
  sfp = 1651				# Sample first pixel
  bfp = 0				# Band first pixel
  #
  # specify the plane, in coordinate space
  # 
  xv = 'all'				# Default X value
  yv = 'all'				# Default Y value
  zv = 'all'				# Default Z value
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
  if type(xv) is str and type(yv) is str and type(zv) is str:
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

def readdata(rvp, rvs):
  #
  # Read in the data volume
  #
  dc = np.fromfile(rvp, dtype='<f', count=-1)
  #
  # Reshape to datacube
  #
  dc = np.reshape(dc, rvs).transpose()
  rvs_x = rvs[2]
  rvs_y = rvs[1]
  rvs_z = rvs[0]
  return dc, rvs_x, rvs_y, rvs_z

def getfilecoords(xv, yv, zv, lfp, sfp, bfp, rvs_X, rvs_Y, rvs_Z):
  err = 0
  #
  # Set data range for 'all'
  #
  if xv == 'all':
    xv = np.arange(lfp, lfp + rvs_X)
  if yv == 'all':
    yv = np.arange(sfp, sfp + rvs_Y)
  if zv == 'all':
    zv = np.arange(bfp, bfp + rvs_Z)
  #
  # translate to pixel space indices
  #
  xvf = xv - lfp
  yvf = yv - sfp
  zvf = zv - bfp
  #
  # Put a more advance log print out here
  #
  if type(xvf) is not int:
    print(len(xvf))
  if type(yvf) is not int:
    print(len(yvf))
  if type(zvf) is not int:
    print(len(zvf))
  #
  # Error Checks
  #
  if np.any(xvf < 0) or np.any(xvf >= rvs_X):
    err = 'Specified X_value is out of bounds for this image'
  if np.any(yvf < 0) or np.any(yvf >= rvs_Y):
    err = 'Specified Y_value is out of bounds for this image'
  if np.any(zvf < 0) or np.any(zvf >= rvs_Z):
    err = 'Specified Z_value is out of bounds for this image'
  return xv, yv, zv, xvf, yvf, zvf, err

def collapsedatacube(dc, xv, yv, zv, xvf, yvf, zvf):
  #
  # Check which dimension is the singleton dimension
  # We assume that the dimension specified as an integer
  # will be the dimension to collapse.
  #
  if type(xv) is int:
    pl = np.squeeze(dc[xvf, yvf[0]:, zvf[0]:])
  elif type(yv) is int:
    pl = np.squeeze(dc[xvf[0]:, yvf, zvf[0]:])
  elif type(zv) is int:
    pl = np.squeeze(dc[xvf[0]:, yvf[0]:, zvf])
  else:
    print('AHHHHHHHHH')
  #
  # The transpose ensures that the first non-singleton dimension in the
  # squeezed matrix (in alpha order) will be interpreted as different
  # columns/x-values
  #
  pl = np.transpose(pl)
  return pl

def getlabels(xv, yv, zv, xvf, yvf, zvf, ast, ai, au):
  err = 0
  d = ['xv', 'yv', 'zv']
  dvc = {"xv": xv, "yv": yv, "zv": zv}		# Dimension value coords
  dvf = {"xv": xvf, "yv": yvf, "zv": zvf}	# Dimenstion value filecoords
  dn = ['X', 'Y', 'Z']				# Dimension names
  #
  # Create empty arrays for labels
  #
  hdn = ''					# Horizontal dimension name
  vdn = ''					# Vertical dimension name
  sdn = ''					# Sliced dimension name
  #
  # The first singleton dimension gets the honor of naming the image
  #
  for dd in range(3): # 0 to 2
    if np.shape(dvc[d[dd]]) == () and sdn == '': 
#      print(dvc[d[dd]])
#      sys.exit()
      sdn = dn[dd]				# Sliced dimension name
      sdc = dvc[d[dd]]				# Sliced dimension coordinate
    else:
      if hdn == '': # Is there a horizontal dimension yet?
        hdn = '{} ({})'.format(dn[dd],au[dd])
        #
        # Calculate the lower and upper bounds in the units of the image's
        # underlying coordinates, which we can get from zero-indexed
        #
        hdl = ast[dd] + ai[dd]*(np.min(dvf[d[dd]]))
        hdu = ast[dd] + ai[dd]*(np.max(dvf[d[dd]]))
      elif vdn == '': # Is the a vertical dimension yet?
        vdn = '{} ({})'.format(dn[dd],au[dd])
        #
        # Calculate the lower and upper bounds in the units of the image's
        # underlying coordinates, which we can get from zero-indexed
        #
        vdl = ast[dd] + ai[dd]*(np.min(dvf[d[dd]]))
        vdu = ast[dd] + ai[dd]*(np.max(dvf[d[dd]]))
      else:
        err = 'At least one dimension must have only one value specified in order to plot as a plane'
  return d, dvc, dvf, dn, hdn, vdn, sdn, sdc, hdl, hdu, vdl, vdu, err
 

def main():
  prog = "SHARAD 3D Plane Viewer"
  vers = "1.0"
  #
  # Parse command line arguments and set default values
  #
  [radar_volume_size, radar_volume_path, axis_units,
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
    #
    # Map values to array indicies
    #
    [x_value, y_value, z_value, x_value_filecoords, y_value_filecoords, \
       z_value_filecoords, err] = getfilecoords(x_value, y_value, z_value, \
       line_first_pixel, sample_first_pixel, band_first_pixel, radar_volume_size_X, \
        radar_volume_size_Y, radar_volume_size_Z)
    if err != 0:
      print(err)
      return
    else:
      plane = collapsedatacube(datacube, x_value, y_value, z_value, 
        x_value_filecoords, y_value_filecoords, z_value_filecoords)
      #
      # Go through the dimension checking sizes to get the labeling correct
      #
      [dim, dim_values_coords, dim_values_filecoords, dim_names,
       horiz_dim_name, vert_dim_name, sliced_dim_name, sliced_dim_coordinate, horiz_dim_lower,
       horiz_dim_upper, vert_dim_lower, vert_dim_upper, err] = getlabels(x_value, y_value, z_value,\
       x_value_filecoords, y_value_filecoords, z_value_filecoords, axis_start, axis_interval, axis_units)
      if err != 0:
        print(err)
        return
      else:
        #
        # Plotting
        #
  
        base_name = basename(radar_volume_path)
        plt.imshow(plane, cmap='gray')
        plt.xlabel(horiz_dim_name)
        plt.ylabel(vert_dim_name)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('dB')
        plt.title(base_name+'_'+str(sliced_dim_name)+str(sliced_dim_coordinate))
        plt.show()
        return

if __name__ == '__main__':
  main()
