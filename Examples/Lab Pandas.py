import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt


satellite_speed= pd.read_excel('data_analysis_example.xlsx' ,0, header = None)
satellite_speed = satellite_speed.iloc[:, 2:]

density_radius = pd.read_excel('data_analysis_example.xlsx', 1, header=None)
density_radius = density_radius.iloc[:, 2:]

satellite_radius = satellite_speed.iloc[0, :]
satellite_velocity = satellite_speed.iloc[1, :]
earth_density = density_radius.iloc[0, :]
earth_radius = density_radius.iloc[1, :]

earth_density_average = earth_density.mean()
earth_radius_average = earth_radius.mean()
print(f"Average density is {earth_density_average:.3f}, average radius is {earth_radius_average:.3f}")

earth_density_std = earth_density.std()
earth_radius_std = earth_radius.std()
print(f"Std density is {earth_density_std:.3f}, std radius is {earth_radius_std:.3f}")

t = 2.78
earth_delta_density = 2.78 * earth_density_std / sqrt(5)
earth_delta_radius = 2.78 * earth_radius_std / sqrt(5)
print("Delta density is {:.3f}, delta radius is {:.3f}".format(earth_delta_density, earth_delta_radius))

#calculate the r inverse and v squared
radius_inverse = 1.0 / satellite_radius
velocity_squared = (satellite_velocity * 1e3 * (1/3600.0) * 1e4) ** 2 * 1e-5

#plot the data
scaled_radius_inverse = radius_inverse * 1e6

# Set the font to Cambria and size 12
plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

# Create figure and set size
f = plt.figure(figsize=(8, 10))

# Show x and y label (you can use latex here)
plt.xlabel(r'$r^{-1}$ / $10^9$ m')
plt.ylabel(r'$v^2$ / $10^5$ m$^2$ s$^{-2}$')

# Enable minor ticks so that we can show a fine grid
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')

# Calculate the polynomical coefficients (last parameters is the number of coefficients)
coeffs = np.polyfit(scaled_radius_inverse, velocity_squared, 1)

# Generate the polynomial function, which when called will take a list of x-values
# and will return the respective y values
poly_function = np.poly1d(coeffs)

# Generate trendline
trendline = poly_function(scaled_radius_inverse)

# Add trendline to plot
plt.scatter(scaled_radius_inverse, velocity_squared)
plt.plot(scaled_radius_inverse, trendline)
plt.savefig('my_plot.png', dpi=300)

# Run polyfit again, this time telling it to return the covariance matrix
coeffs, V = np.polyfit(scaled_radius_inverse, velocity_squared, 1, cov=True)
gradient = coeffs[0]
intercept = coeffs[1]

# Compute the gradient and intercept error
gradient_error = np.sqrt(V[0][0])
intercept_error = np.sqrt(V[1][1])

# Aside: If you also want the correlation coefficient, you can:
correlation = np.corrcoef(scaled_radius_inverse, velocity_squared)[0, 1]

print(f"Gradient is {gradient:.3f}, with error {gradient_error:.3f}")
print(f"Intercept is {intercept:.3f}, with error {intercept_error:.3f}")
print(f"Correlation coefficient is {correlation:.3f}")

plt.show()

