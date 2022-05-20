import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# importing data
data = pd.read_excel(`Experiment 5.xlsx')
# defining variables and constants
A = np.asarray(data[`A'])
Ap = np.asarray(data[`'Ap'])
B = np.asarray(data[`B'])
Bp = np.asarray(data[`Bp'])
d = 1/600000
n = np.array([6,5,4,3])
dA = 1/120
dB = 1/120

# finding the angles from the repeated readings
theta1 = np.absolute(A-Ap)/2
theta2 = np.absolute(B-Bp)/2
# finding the average of the angles
theta = (theta1 + theta2)/2
# finding the error for each value
dt = np.sqrt((theta1*dA**2) + (theta2*dB**2))
dtf = np.sqrt((theta*dt**2) + (theta*dt**2))
dw = (d*(np.cos(theta))*dtf)
dl =(1/np.sqrt(np.abs(dw)))

# finding the wavelength
wavelength = d*np.sin(np.deg2rad(theta))

# defining plotting arrays
Y = 1/wavelength
X = ((1/2**2)-1/(n**2))

# determining the line of best fit
coeffs, cov = np.polyfit(X, Y, deg=1, cov=True)
poly_funct= np.poly1d(coeffs)
trendline = poly_funct(X)
# defining the error of Rydberg's constant
error = np.sqrt(cov[0][0])
print(f``Rydberg's constant is {coeffs[0]:.2e}
         with an error of {error:.2e}")

# finding the accuracy and the precision
accuracy = (coeffs[0]/1.097e7)*100
precision = (error/coeffs[0])*100
print(f`The accuracy was found to be {accuracy:.2f}%
        and a precision of {precision:.2f}%')

# defining the size of the figure
f = plt.figure(figsize=(7.3, 10.7))

# defining the plot line, points, error bars
plt.errorbar(X, Y, xerr=0, yerr=dl, fmt=`o', 
             color=`k', elinewidth=2, capthick=2, capsize=5,
             ecolor=`grey', label=`Data Points')
plt.plot(X, trendline, color=`k', label=`Fit')
# defining axis labels, title, grid, legend and showing plot
plt.minorticks_on()
plt.grid(b=True, which=`major', linestyle=`-')
plt.grid(b=True, which=`minor', linestyle=`--')
plt.xlabel(r`$(\frac{1}{2^2}-\frac{1}{n^2})$')
plt.ylabel(r`$\frac{1}{\lambda}$/$\frac{1}{m}$')
plt.title(r`A plot of $\frac{1}{\lambda}$ 
            vs $(\frac{1}{2^2}-\frac{1}{n^2})$')
plt.legend()
# removing wasted space from graph boundaries
plt.tight_layout()
# saving plot
plt.savefig(`l vs x.png', dpi=800)
plt.show()
