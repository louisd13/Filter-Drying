import numpy as np
import statistics
import matplotlib.pyplot as plt

# starting point of the mean difference in [s]
start = 1107 

with open(r'C:\Users\duval\Documents\EPFL\MA2\PDS\Semestre 2\Sechage filtres stx + debut de carac POC\1.8A_270s_2Temp.txt') as f:
    lines = f.readlines()
    length = len(lines)

    # Extract var1 and var2 values from each line
    var1_values = []
    var2_values = []
    for i in range(start,len(lines),3):
        var1_values.append(float(lines[i].strip()))
        var2_values.append(float(lines[i+1].strip()))

    # Calculate the differences between var1 and var2
    differences = [var1 - var2 for var1, var2 in zip(var1_values, var2_values)]

    # Calculate the mean difference between var1 and var2
    mean_difference = sum(differences) / len(differences)

    print(f"The mean difference between Internal and External temperature is: {mean_difference}")
