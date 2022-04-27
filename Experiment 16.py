import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import *
from math import sqrt

# importing data and defining constants
data = pd.read_excel('Experiment 16.xlsx')
x = np.asarray(data['x'])/100
y = np.asarray(data['y'])/100
V = 1500
I = np.asarray(0.25 * (data['CH1'] + data['CH2'] + 
               data['CH3'] + data['CH4']))
r = 0.065
N = 320
u = 1.257e-6
ae = 1.76e11

# defining the constant
c = ((2*V*r**2)/(0.72**2 * u**2 * N**2))
# defining the co-oridnate values
X = np.array(((2*y)/(x**2 + y**2))**2)
Y = np.array(I**2)
# defining the error for I
dI = 3.18 * np.std([data['CH1'], data['CH2'], 
                    data['CH3'], data['CH4']],
                    axis=0)/np.sqrt(4)
# as std=0 minimum readability is used
dX = 0.01

# finding the equation of the line of best fit
coeffs, cov = np.polyfit(X, Y, 1, cov=True)
poly_function = np.poly1d(coeffs)
# defining the line of best fit
trendline = poly_function(X)
# definfing the value of the gradient
m = coeffs[0]
# finding the error of the gradient
dm = np.sqrt(cov[0][0])

# calculating the specific charge of an electron
e = c/(m)

# doing the partial derivative
def merr(d, e, dm):
    a = Symbol('a')
    b = Symbol('b')
    equation = a/b
    diff_b = Derivative(equation, b)
    db = diff_b.doit()
    de = db.subs({a : c, b : m}).evalf()
    return de*dm
de = abs(merr(c, m, dm))
print(f'The specific charge of electrons is {e:.2e}, 
        with an error of {de:.2e}')
# finding the precision and accuracy of the values of 
    the value obtained
precision = (de/e) * 100
accuracy = (e/ae) * 100
print(f'With a precision of {precision:.2f}% 
        and an accuracy of {accuracy:.2f}%')

# defining the fonts and sizes to be used
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the size of the figure
f = plt.figure(figsize=(7.3, 10.7))

# defining the plot and showing it
plt.errorbar(X, Y, xerr=dX, yerr=dI, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.plot(X, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$Co$-$oridnates^2$/m$^2$')
plt.ylabel(r'$I^2$/A$^2$')
plt.title(r'$I^2$/A$^2$ vs $Co$-$ordinates^2$/m$^2$')
plt.savefig('I2vsCo-or2.png', dpi=800)
plt.legend()
plt.show()
