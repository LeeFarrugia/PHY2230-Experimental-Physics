import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import *
from math import sqrt
 
#importing data to be read and defining variables
data = pd.read_excel('Experiment 13.xlsx')
r = data['r/m'].mean()
x = data['x1/m'].mean(), data['x2/m'].mean(), data['x3/m'].mean(),       
    data['x4/m'].mean(), data['x5/m'].mean()
T = data['f1/N'].mean(), data['f2/N'].mean(), data['f3/N'].mean(), 
    data['f4/N'].mean(), data['f5/N'].mean()
rho = 8400
deltar = 2.57 * (np.std(data['r/m'])/np.sqrt(6))
x2 = np.power(x, 2)
constant = 4 * np.pi * rho
deltax = 2.78 * np.array([np.std(data['x1/m']),np.std(data['x2/m']),
                np.std(data['x3/m']), np.std(data['x4/m']),
                np.std(data['x5/m'])])/np.sqrt(5)
deltax2 = 2 * deltax
# as T has no std, minimum readability is used
deltaT = 1
 
# finding the straight line equation with the data given
coeffs, cov = np.polyfit(T, x2, 1, cov=True)
poly_function = np.poly1d(coeffs)
trendline = poly_function(T)

# gradient and error called
print(f'The gradient is: {coeffs[0]}, with 
        an error of: {np.sqrt(cov[0][0])}')
# storing the coefficients
m = coeffs[0]
deltam = np.sqrt(cov[0][0])
 
# calculating the frequency
freq = np.sqrt(1/ (constant * r**2  * coeffs[0]))
 
# partial derivation for the the frequency error
def freqerr(d, e, f, deltar, deltam):
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    equation = (1/(c * (a**2) * b))**0.5
    diff_a = Derivative(equation, a)
    diff_b = Derivative(equation, b)
    da = diff_a.doit()
    db = diff_b.doit()
    dr = da.subs({a : d, b : e, c : f}).evalf()
    dm = db.subs({a : d, b : e, c : f}).evalf()
    return (dr*deltar)**2 + (dm*deltam)**2
 
# storing and calculating the final value of the frequency error
nsferr = freqerr(r, m, constant, deltar, deltam)
ferr = sqrt(nsferr)
 
# calculating the precision and accuracy of the experiment
print(f'The frequency is: {freq}Hz with an error of: {ferr}Hz')
precision = ferr/freq * 100
accuracy = ((freq/512)-1) * 100
# printing out the values obtained
print(f'The accuracy of the experiment is {accuracy}%, 
        and the precision is {precision}%')
 
# defining the fonts and sizes to be used
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'
 
f = plt.figure(figsize=(7.3, 10.7))
 
plt.errorbar(T, x2, xerr=deltaT, yerr=deltax2, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5, ecolor='grey',
             label='Data Points')
plt.plot(T, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$T$/N')
plt.ylabel(r'$x^2$/m$^2$')
plt.title(r'$x^2/$m$^2$ vs $T$/N')
plt.savefig('x2vsTgraph.png', dpi=800)
plt.legend()
plt.show()
