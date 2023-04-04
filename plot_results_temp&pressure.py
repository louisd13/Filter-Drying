import numpy as np
import matplotlib.pyplot as plt

# Load the data from the text file
data = np.loadtxt(r"C:\Users\duval\Documents\EPFL\MA2\PDS\Semestre 2\Tests Pression & °C\1.8A_180s_53_Wet_#6.txt")

# Extract the data for the first plot
y1 = data[::2]

# Extract the data for the second plot
y2 = data[1::2]

# Create a figure and an axis
fig, ax = plt.subplots()

# Plot the first set of data on the first y-axis
ax.plot(y1, color='blue', label='Température')

# Create a twin axis
ax2 = ax.twinx()

# Plot the second set of data on the twin axis
ax2.plot(y2, color='red', label='Pression')

# Set the labels for the axes and the legend
ax.set_xlabel('Secondes [s]')
ax.set_ylabel('Température [°C]')
ax2.set_ylabel('Pression [Bar]')
ax.legend()

# Show the plot
plt.show()