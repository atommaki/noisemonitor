#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

log_file_path = 'noise_levels.log'  # Path to your log file

# Initialize an empty list to store the data
data = []

# Read and parse the log file
with open(log_file_path, 'r') as file:
    for line in file:
        if ': Bands: ' in line:
            parts = line.strip().split(': Bands: ')[1].split(' | ')
            timestamp = line.split(': Bands: ')[0].strip()
            levels = [float(p.split(': ')[1]) for p in parts]
            data.append({'timestamp': timestamp, **{f'Band {i+1}': level for i, level in enumerate(levels)}})

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Convert timestamp to datetime and set it as index
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Plotting
plt.figure(figsize=(15, 8))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)

plt.xlabel('Time')
plt.ylabel('Noise Level')
plt.title('Noise Levels Over Time')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

