""" 
 * @file plot_results_2temp.py
 * @author Louis Duval
 * @brief Plotting and prints for internal and external thermistor delta determination
 * @version 0.1
 * @date 2023-06-29
 *
 * @copyright Copyright (c) 2023
 *
  """
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time

exp_temp = 55


def calculate_slope(temperature, time):
    # Calculate the slope using the formula: slope = (y2 - y1) / (x2 - x1)
    slope = (temperature[-1] - temperature[0]) / (time[-1] - time[0])
    return slope


def find_time_target_temp(temperature_data, target_temp):
    for index, temperature in enumerate(temperature_data):
        if temperature >= target_temp:
            return index
    

 
file_path = r"C:\Users\duval\Documents\EPFL\MA2\PDS\Semestre 2\Sechage filtres stx + debut de carac POC\1.8A_STX_120s_55_2Temp_2.txt"

# Load the data from the text file
data = np.loadtxt(file_path)

# Extract the data for the first plot
y1 = data[::3]
time = np.arange(len(y1))  # Assuming the time is evenly spaced

# Extract the data for the second plot
y2 = data[1::3]

# Extract the data for the third plot
y3 = data[2::3]

target_temp_index = 3*find_time_target_temp(y1,exp_temp)

print("Index :", target_temp_index)
print("Seconds to target temp", find_time_target_temp(y1,exp_temp))


with open(file_path) as f:
    lines = f.readlines()
    length = len(lines)

    # Extract var1 and var2 values from each line
    var1_values = []
    var2_values = []
    for i in range(target_temp_index, len(lines), 3):
        var1_values.append(float(lines[i].strip()))
        var2_values.append(float(lines[i+1].strip()))

    # Calculate the differences between var1 and var2
    differences = [var1 - var2 for var1, var2 in zip(var1_values, var2_values)]

    # Calculate the mean difference between var1 and var2
    mean_difference = sum(differences) / len(differences)

    print(f"The mean difference between internall and external temperature [°C]: {mean_difference}")


# Create a figure and an axis
fig, ax = plt.subplots()

# Plot the first set of data on the first y-axis
ax.plot(y1, color='blue', label="Intern")
ax.plot(y2, color='red', label="Extern")

# Create a twin axis
ax2 = ax.twinx()
ax2.plot(y3, color='yellow', label='Switch')

# Set the labels for the axes and the legend
ax.set_xlabel('Seconds [s]')
ax.set_ylabel('Temperature [°C]')
ax2.set_ylabel('Switch')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
ax2.legend(loc= 'upper center', bbox_to_anchor=(0.5, 1.08), ncol=2)

print("Int max",max(y1))
print("Ext Max", max(y2))

# Show the plot
plt.show()