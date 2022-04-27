import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# importing data
data = pd.read_excel('Experiment 4.xlsx')
# defining relevant data
h1 = np.asarray(data['h1']/100)
h2 = np.asarray(data['h2']/100)
d = np.asarray(data['d']/100)

# determining the eqaution of line of best fit
coeffs, cov = np.polyfit(d, h1, deg=1, cov=True)
poly_function = np.poly1d(coeffs)
trendline = poly_function(d)

# defining the gradient and error of gradient
m = coeffs[0]
dm = np.sqrt(cov[0][0])
# displaying values of gradient and error
print(f'Gamma is {m:.2f} with an error of {dm:.2f}')

# defining the minimum readability of the meter ruler
dh1 = 0.01
dd = 0.01

# finding the precision and accuracy 
  of the values of the value obtained
precision = (dm/m) * 100
accuracy = (m/1.4) * 100
print(f'With a precision of {precision:.2f}% 
        and an accuracy of {accuracy:.2f}%')

# defining the fonts and sizes to be used
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the size of the figure
f = plt.figure(figsize=(7.3, 10.7))

# plotting errorbars and line of best fit
plt.errorbar(d, h1, xerr=dd, yerr=dh1, fmt='o', color='k',
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.plot(d, trendline, color='k', label='Fit')
# defining axis labels, title, grid, legend and showing plot
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$(h_1-h_2)$/m')
plt.ylabel(r'$h_1$/m')
plt.title(r'A plot of $h_1$ vs $(h_1-h_2)$')
plt.legend()
plt.savefig('h1vsd.png', dpi=800)
plt.show()
