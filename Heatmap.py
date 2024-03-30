# -*- coding: utf-8 -*-
"""
author: Martijn Sitters

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import pandas as pd


file = r"example file"

data_df = pd.read_excel(file)
data_df = data_df["gemiddelde"]

num_rows = 3
num_cols = data_df.shape[0] // num_rows
data = data_df.iloc[:num_rows * num_cols].values.reshape(num_rows, num_cols)

plt.figure(figsize=(16, 9))
plt.imshow(data, cmap = "turbo", interpolation='bicubic', aspect='auto')

for i in range(num_rows):
    for j in range(num_cols):
        plt.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', color='black')

plt.colorbar(label='nagalmtijd [s]')
plt.title('Heatmap Lab C')
plt.xlabel('Breedte')
plt.ylabel('Lengte')

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().tick_params(axis='both', which='both', length=0)

plt.xticks([])
plt.yticks([])

plt.text(num_cols/2 - 0.6, -0.65, '15m', ha='center', va='center', size="15")
plt.text(-0.6, num_rows/2 - 0.615, '8m', ha='center', va='center', rotation=90, size="15")

plt.ylim(-0.7, num_rows - 0.5)
plt.xlim(-0.7, num_cols - 0.5)

plt.show()
