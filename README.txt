This is a Python 3+ version of the sharad_3d_planeviewer written by Daniel Politte
and ported to Python by Matthew Perry.

SHARAD 3D Plane Viewer 1.0

optional arguments:
  -h, --help  show this help message and exit
  -rvp RVP    Path to the radar volume  {Default: ./PLANUM_BOREUM_3D_TIME.DAT}
  -xv XV      X-value slice. Integer or all {Default: All}
  -yv YV      Y-value slice. Integer or all  {Default: All}
  -zv ZV      Z-value slice. Integer or all  {Default: All}

I recommend placing a symbolic link inside the directory you are working from or using a static
directory to store the 3D volumes as they are quite large. If you place a symbolic link inside your
working directory, you will not need to use the -rvp optional argument everytime you run the program.

Only one of the following is required to run the program as long as the radar volume is in the working
directory: -xv, -yv, or -zv.

For example if you want to create a slice along line (X axis) 3500:
  sharad_3d_planeViewer.py -xv 3500
For example if you want to create a slice along sample (Y axis) 1660:
  sharad_3d_planeViewer.py -yv 3500
For example if you want to create a slice along band (Z axis) 100:
  sharad_3d_planeViewer.py -zv 100
