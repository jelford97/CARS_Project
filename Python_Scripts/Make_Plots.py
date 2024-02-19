from pymakeplots import pymakeplots

file='/Users/jelford/Documents/PhD_Work/CARS_Data/HE1353/HE13531917_clean_co.image.fits'
plotter=pymakeplots(cube=file)
plotter.rmsfac=5
plotter.chans2do=[90,125]
#plotter.maxvdisp=140
#plotter.obj_ra,plotter.obj_dec=209.152925, -19.529187
plotter.make_moments(mom=[0,1,2])