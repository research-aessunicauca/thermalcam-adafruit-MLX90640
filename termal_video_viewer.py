import time
import os
import numpy as np 
import matplotlib.pyplot as plt
from pathlib import Path
import json
from scipy import ndimage


# function to add to JSON
def read_json_file(filename='data.json'):
    mode = 'r+' if os.path.exists(filename) else 'w'
    with open(filename,mode) as file:
        # First we load existing data into a dict.
        file_data = []
        try:
            file_data = json.load(file)
        except:
            print('error loading file')
        
        return file_data


mlx_shape = (24,32)

# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label
t_array = []

def show_frame(frame):
    data_array = np.asarray(frame["data"])
    data_array = ndimage.zoom(data_array, 10)
    therm1.set_data(np.fliplr(data_array)) # flip left to right
    therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
    #cbar.on_mappable_changed(therm1) # update colorbar range
    #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC',
        #            bbox_inches='tight') # comment out to speed up
    plt.pause(frame["frame_render_time"]*5) # required

file_name = "2022-07-03T165157.057483.json"
file_path = Path("records/") / file_name

record_data = read_json_file(file_path)

for frame in record_data:
    try:
        print(frame)
        show_frame(frame)
    except ValueError:
        continue
