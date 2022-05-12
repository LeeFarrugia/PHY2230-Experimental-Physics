import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import data from excel file
data = pd.read_excel('Experiment 11.xlsx', 2)

# to find averages of l
average_l = data['l1'] + data['l2'] + data['l3'] + data['l4']
average_l /= 4

# defining the y-axis and x-axsis values
y = np.hstack((0.5-average_l)/average_l)
x = np.asarray(data['R '])

# to obtain line of best fit and covariance matrix
coeffs, cov = np.polyfit(x, y, deg=1, cov=True)
poly_function = np.poly1d(coeffs)
trendline = poly_function(x)

# otaining the gradient and its error
gradient = (coeffs[0])**-1
gradient_error = (np.sqrt(cov[0][0]))

print(f'Gradient is {gradient:.3f}, with error {gradient_error:.3f}')

# finding the error of l
std_l = np.std([data['l1'], data['l2'], data['l3'], data['l4']], axis=0, ddof=1)
delta_l = 3.18 * std_l / np.sqrt(4)

# fucntion to calculate the y error
def yerror(l, delta_1):
    dy = np.sqrt(((-0.5/l**2) * (delta_l))**2)
    print(dy)

delta_x = 1
delta_y = yerror(y, delta_l)

# finding the accuracy and precision values
accuracy = ((gradient/10)-1)*100
precision = (gradient_error/gradient)*100

print(f'The accuracy is {accuracy:.2f}% and a precision {precision:.2f}%')

# setting the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the foigure size
f = plt.figure(figsize=(8, 10))

# plotting graph, errorbars
plt.errorbar(x, y, xerr=delta_x, yerr=delta_y,
             fmt='o', color='k', elinewidth=2, capsize=7,
             capthick=2, ecolor='gray', label='Data Points')
plt.plot(x, trendline, 'k', label='Fit')
plt.minorticks_on()
plt.grid(visible=True, which='major', linestyle='-')
plt.grid(visible=True, which='minor', linestyle='--')
plt.title(r'A graph of $\frac{0.5-l}{l}$ in m vs R in $\Omega$')
plt.xlabel(r'R/ $\Omega$')
plt.ylabel(r'$\frac{50-l}{l}$/ m')
plt.tight_layout()
plt.savefig('Plot.png', dpi=800)
plt.show()
