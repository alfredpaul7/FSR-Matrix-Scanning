#Python heatmap code for 32x64 with SPI protocol
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# --- Settings ---
COM_PORT = 'COM6'
BAUD_RATE = 921600
ROWS, COLS = 32, 64  # Updated for your 32x64 display
THRESHOLD = 40       
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    ser.flushInput()
    print(f"Connected to {COM_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()
fig, ax = plt.subplots(figsize=(10, 8)) # Wider figure for 32x64
data_matrix = np.zeros((ROWS, COLS))
# Using 'Gaussian' interpolation for that smooth heatmap look
im = ax.imshow(data_matrix, cmap='jet', interpolation='gaussian', vmin=0, vmax=1500)
plt.colorbar(im)
# Formatting labels
ax.set_xticks(np.arange(COLS)) # Labels every 4 units for readability
ax.set_yticks(np.arange(ROWS))
ax.set_xticklabels([str(i+1) for i in range(COLS)], fontsize=6)
ax.set_yticklabels([str(i+1) for i in range(ROWS)], fontsize=6)
ax.xaxis.tick_top()
def update(frame):
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line: return [im]  
            # Convert the long string of 2048 values into a list of integers
            raw_data = [int(x) for x in line.split(',') if x.strip()]
            if len(raw_data) == 2048:
                # Process Left Sensor (Values 0-1023)
                tile_left = np.array(raw_data[:1024]).reshape((32, 32)).T

                # Process Right Sensor (Values 1024-2047)
                tile_right = np.array(raw_data[1024:]).reshape((32, 32)).T
            
                # Combine into the 32x64 canvas
                full_canvas = np.zeros((32, 64))
                full_canvas[:, :32] = tile_left
                full_canvas[:, 32:] = tile_right
                full_canvas[full_canvas < THRESHOLD] = 0
                im.set_data(full_canvas)
              
            else:
                # This helps you debug if you aren't sending enough data
                print(f"Data received but length is {len(raw_data)} instead of 2048")
              
        except Exception as e:
            print(f"Parsing error: {e}")
    return [im]
ani = FuncAnimation(fig, update, interval=1, blit=True, cache_frame_data=False)
plt.tight_layout()
plt.show()
ser.close()