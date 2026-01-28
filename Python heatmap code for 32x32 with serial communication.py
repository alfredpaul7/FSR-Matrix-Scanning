#Python heatmap code for 32x32 with serial communication 
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Settings Area ---
COM_PORT = 'COM6'
BAUD_RATE = 115200
ROWS = 32
COLS = 32

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    ser.flushInput()
    print(f"Successfully connected to {COM_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Setup Figure and Axis
fig, ax = plt.subplots(figsize=(10, 8))
data_matrix = np.zeros((ROWS, COLS))

# Render the heatmap
im = ax.imshow(data_matrix, cmap='jet', interpolation='gaussian', vmin=0, vmax=1500)

# --- COLORBAR SETTINGS ---
# Create the colorbar and remove the numeric labels (0-1400)
cbar = plt.colorbar(im)
cbar.set_ticks([]) 

# --- ADDING ROW AND COLUMN NUMBERING ---
ax.set_xticks(np.arange(COLS))
ax.set_yticks(np.arange(ROWS))

# Label every single sensel (1-indexed)
ax.set_xticklabels([str(i+1) for i in range(COLS)], fontsize=8)
ax.set_yticklabels([str(i+1) for i in range(ROWS)], fontsize=8)

# Move X-axis labels to the top
ax.xaxis.tick_top()

# Add Grid to make it look like a matrix
ax.set_xticks(np.arange(-.5, COLS, 1), minor=True)
ax.set_yticks(np.arange(-.5, ROWS, 1), minor=True)
ax.grid(which='minor', color='white', linestyle='-', linewidth=0.5)

def update(frame):
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line: return [im]
            
            raw_data = [int(x) for x in line.split(',') if x.strip()]
            
            if len(raw_data) == ROWS * COLS:
                # 1. Reshape
                new_matrix = np.array(raw_data).reshape((ROWS, COLS))
                
                # 2. Fix Horizontal/Vertical Swap
                new_matrix = new_matrix.T
                
                # 3. FIX INVERSION
                # Note: I removed the quadruple flips (ud/lr/ud/lr) as they cancel each other out.
                # If your image appears upside down or mirrored, uncomment only ONE of these:
                # new_matrix = np.flipud(new_matrix) # Use this if image is upside down
                # new_matrix = np.fliplr(new_matrix) # Use this if image is mirrored
                
                im.set_data(new_matrix)
            else:
                pass
        except Exception as e:
            print(f"Parsing error: {e}")
    return [im]

ani = FuncAnimation(fig, update, interval=20, blit=True, cache_frame_data=False)
plt.tight_layout()
plt.show()
ser.close()
