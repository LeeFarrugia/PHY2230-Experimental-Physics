import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_excel('fusing_current_data.xlsx', 0)

# Calculate average current for each row
average_I = data['I1/A'] + data['I2/A'] + data['I3/A']
average_I /= 3

# Calculate average diameter for each row
average_d = data['d1/mm'] + data['d2/mm'] + data['d3/mm'] + data['d4/mm'] + data['d5/mm'] + data['d6/mm']
average_d /= 6

standard_deviation = np.std([data['I1/A'], data['I2/A'], data['I3/A']], axis=0, ddof=1)
delta_I = 3.182 * standard_deviation / np.sqrt(3)

standard_deviation = np.std([data['d1/mm'], data['d2/mm'], data['d3/mm'], data['d4/mm'], data['d5/mm'], data['d6/mm']], axis=0, ddof=1)
delta_d = 2.447 * standard_deviation / np.sqrt(6)

delta_I /= average_I
delta_d /= average_d

# Compute the logs of array which do not have invalid values
average_I = np.log(average_I)
average_d = np.log(average_d)

# Calculate the polynomical coefficients (last parameters is the number of coefficients)
coeffs = np.polyfit(average_d, average_I, 1)

# Generate the polynomial function, which when called will take a list of x-values
# and will return the respective y values
poly_function = np.poly1d(coeffs)

# Generate trendline
trendline = poly_function(average_d)

# Set the font to Cambria and size 12
plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

# Create figure and set size
f = plt.figure(figsize=(8, 10))

# Show the data
plt.errorbar(average_d, average_I, xerr=delta_d, yerr=delta_I, fmt='o', color='k', elinewidth=2, capsize=5, capthick=2, ecolor='gray')

# Show the trendline
plt.plot(average_d, trendline, 'k--')

# Enable minor ticks so that we can show a fine grid
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')

# Display labels
plt.xlabel(r"$\ln(d)$")
plt.ylabel(r"$\ln(I)$")

plt.show()