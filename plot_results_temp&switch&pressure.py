""" 
 * @file plot_results_temp&switch&pressure.py
 * @author Louis Duval
 * @brief Plotting and prints
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

# if using an encapsulated filter : 1
encapsulated = 0
# to tune in function of initial heat pulse (make it larger that regular pulse but lower than initial)
min_time = 50;
# Expiremental temperature wanted
exp_temp = 65

# Deltas previously determined (depend on the system)
def deltas(target_temp, encapsulated):
    if(encapsulated):
        if (target_temp==45):
            return 4.3
        if(target_temp==55):
            return 5.9
        if(target_temp==65):
            return 7.7
    else:
        return 0

# Target temperature of the system read by the thermistor (if external control != exp_temp)
target_temp = int(exp_temp - deltas(exp_temp,encapsulated))
# path to text file
file_path = r"C:\Users\duval\Documents\EPFL\MA2\PDS\Semestre 2\Sechage filtres disk 1 data\2A_2FSP_65_t1_3.txt" 

# Simulates internal temperature
def intern_temp(temps, start, delta):
    y = [0] * len(temps)  # Create a new array filled with 0
    
    for i in range(start, len(temps)):
        y[i] = temps[i] + delta  # Add delta to values from the start index onwards
    
    return y

# Average of starting temperature
def starting_temp(temps):
    ten_values = temps[:10]
    avg_temp = sum(ten_values) / 10
    
    return avg_temp

# Absolute mean difference between temp and target_temp in [%]
def temp_precision(temps, target_temp, start_index=0, stop_index=None):
    y = temps[start_index:stop_index]
    precision = (sum([abs(temperature - target_temp) for temperature in y]) / (len(y) * target_temp))*100
    
    return precision

#Returns the time in [s] it attained target_temp for the first time
def find_time_target_temp(temp_data, target_temp):
    for index, temp in enumerate(temp_data):
        if temp >= target_temp:
            return index

# % of time the switch is on
def duty_cycle(heating_periods):
    on_time = sum(heating_periods)
    total_time = len(heating_periods)
    duty_cycle = (on_time / total_time) * 100
    return duty_cycle

# Returns slope from the first initial switch on period until some time_threshold
def get_slope(temps, switch, time_threshold):
    slope_arr = []

    switch_start = None
    for i, switch_value in enumerate(switch):
        if switch_value == 1:
            if switch_start is None:
                switch_start = i
        else:
            if switch_start is not None and i - switch_start >= time_threshold:
                slope_arr.extend(temps[switch_start:i])
                slope = (temps[i - 1] - temps[switch_start]) / (i - switch_start - 1)
                return slope
            switch_start = None

    return slope

# Returns the first Max temperature slope [°C/s] after the first initial switch on (when switch is off for first time)
def get_inertia(temps, switch_values, time_threshold):
    switch_on_val = []
    switch_off_val = []
    switch_on = False
    switch_off = False

    for temp, switch in zip(temps, switch_values):
        if switch == 1:
            switch_on = True
            if switch_off:
                switch_off = False
                break
        elif switch == 0:
            if switch_on:
                switch_off = True
        if switch_off:
            switch_off_val.append(temp)
                
    return switch_off_val

# Returns the time at which the pressure spikes, in Sterivex case the end of drying
def find_pressure_spike_time(pressure_array):

    # Find the index where pressure starts increasing significantly
    for i in range(60, len(pressure_array)):
        if pressure_array[i] > -0.35:
            return i

# Load the data from the text file
data = np.loadtxt(file_path)

# Extract the data for the first plot
y1 = data[::3]
time = np.arange(len(y1))

# Extract the data for the second plot
y2 = data[1::3]

# Extract the data for the third plot
y3 = data[2::3]

# Time we attain the temperature we want 
time_to_target = find_time_target_temp(y1,target_temp)

# Add an estimation of intern temperature (if controlled by external temperature)
if(encapsulated):
    y4 = intern_temp(y1,time_to_target,deltas(exp_temp,encapsulated))

# Create a figure and an axis
fig, ax = plt.subplots()

# Plot the first set of data on the first y-axis & simulates internal temperature
ax.plot(y1, color='blue', label='Temperature')
if(encapsulated):
    ax.plot(range(time_to_target, len(y4)), y4[time_to_target:], color='red', label = 'Internal Temperature')
# Create a twin axis
ax2 = ax.twinx()
ax2.plot(y2, color='purple', label='Pressure') 
ax2.plot(y3, color='yellow', label="Switch")


# Set the labels for the axes and the legend
ax.set_xlabel('Secondes [s]')
ax.set_ylabel('Température [°C]')
ax2.set_ylabel('Pressure [Bar]')
# Position the legend above the plots
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
ax2.legend(loc= 'upper center', bbox_to_anchor=(0.5, 1.08), ncol=2)

slope = get_slope(y1,y3,min_time)
inertia = get_inertia(y1,y3,min_time)
stop_time = find_pressure_spike_time(y2)

#prints
print("Slope of initial temperature increase [°C/s]:", slope)
print("First max inertia slope",(max(inertia)-inertia[0])/inertia.index(max(inertia)))
print("External target temp", target_temp)
print("Starting temperature", starting_temp(y1))
print("Time to target temperature in seconds", time_to_target)
print("Imprecision in %", temp_precision(y1,target_temp,time_to_target,stop_time)) 
print("Heat on in % of time  :", duty_cycle(y3))
print("End of drying in [s]:", find_pressure_spike_time(y2))
print("Total time [s]: ", len(y1))
if(encapsulated):
    print("Internal max temperature", max(y4))


# Show the plot
plt.show()