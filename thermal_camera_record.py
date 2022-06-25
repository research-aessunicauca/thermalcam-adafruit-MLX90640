import time,board,busio
import os
import numpy as np 
import adafruit_mlx90640 
import matplotlib.pyplot as plt
import datetime
from pathlib import Path

# Python program to update
# JSON


import json


# function to add to JSON
def append_on_json(new_data, filename='data.json'):
    mode = 'r+' if os.path.exists(filename) else 'w'
    with open(filename,mode) as file:
        # First we load existing data into a dict.
        file_data = []
        try:
            file_data = json.load(file)
        except:
            print('error loading file')
        
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
        print('append data')

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ # set refresh rate
mlx_shape = (24,32)

# setup the figure for plotting
plt.ion() # enables interactive plotting
fig,ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
cbar = fig.colorbar(therm1) # setup colorbar for temps
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []

def show_frame(data_array):
    
    therm1.set_data(np.fliplr(data_array)) # flip left to right
    therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
    plt.pause(0.001) # required
    cbar.on_mappable_changed(therm1) # update colorbar range
    #fig.savefig('mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC',
        #            bbox_inches='tight') # comment out to speed up
    

current_utc_date = datetime.datetime.utcnow().isoformat()
file_path = Path("records/") / (current_utc_date+".json")
start_time = time.monotonic()
frames = []


while True:
    t1 = time.monotonic()
    
    try:
        mlx.getFrame(frame) # read MLX temperatures into frame va    
        data_array = np.reshape(frame,mlx_shape) # reshape to 24x32
        
        current_mono = time.monotonic()
        current_time = current_mono-start_time
        frame_render_time = current_mono-t1
        data_frame = {"time":current_time, "frame_render_time":frame_render_time, "data": data_array.tolist()}
        append_on_json(data_frame, file_path)
        #show_frame(data_array)
        #t_array.append(frame_render_time)
        #print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue # if error, just read again 
