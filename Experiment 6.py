import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from math import sqrt

#importing the data
data = pd.read_excel('Experiment 6.xlsx')
#defining constants
temp = (np.asarray(data['heating 1'] + data['cooling 1'] +
       data['heating 2'] + data['cooling 2'])/4) + 273.15
dl = np.asarray(data['dl1'] + data['dl2'] + 
     data['dl3'] + data['dl4'])/40
l0 = np.asarray(data['l'])
l0 = l0[~np.isnan(l0)]
l0a = np.average(l0)

#defining the y and x axis
Y = dl
X = temp

#defining the variation of each constant
dl0 = 4.30 * np.std(data['l'])/np.sqrt(3)
dYstd = np.std([data['dl1'], data['dl2'], 
        data['dl3'], data['dl4']], axis=0, ddof=1)
dY = (3.18/np.sqrt(4)) * dYstd
dX = 0.25 * (np.asarray(data['dt1'] + data['dt2'] + 
     data['dt3'] + data['dt4']) + 273.15)/4

#defining the straight line to be plotted
coeffs, cov = np.polyfit(X, Y, deg=1, cov=True)
poly_func = np.poly1d(coeffs)
trendline = poly_func(X)
m = coeffs[0]
dm = np.sqrt(cov[0][0])

#finding the error of the coefficient
def merror(c, d, dm, dl0):
    a = Symbol('a')
    b = Symbol('b')
    equation = a/b
    diff_a = Derivative(equation, a)
    diff_b = Derivative(equation, b)
    da = diff_a.doit()
    db = diff_b.doit()
    dc = da.subs({a : c, b : d}).evalf()
    dd = db.subs({a : c, b : d}).evalf()
    return (dc*dm)**2 + (dd*dl0)**2

err = sqrt(merror(m, l0a, dm, dl0))
print(f'The thermal coefficient of the material is 
        {coeffs[0]/l0a:.2e}K\u207b\u00b9 \u00b1 
        {err:.2e}K\u207b\u00b9 ')
        
#defining the precision and accuracy
precision = (err/(coeffs[0]/l0a))*100
accuracy = (((coeffs[0]/l0a)/(11e-6)))*100
print(f'The accuracy is {accuracy:.2f}% and 
        the precision is {precision:.2f}%')

#defining the plot size and axis
plt.figure(figsize=(7.3, 10.7))
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.xticks(X)

#plotting the error bars
plt.errorbar(X, Y, xerr=dX, yerr=dY, fmt='o', 
             color='k', elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
#plotting the straight line
plt.plot(X, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(visible=True, which='major', linestyle='-')
plt.grid(visible=True, which='minor', linestyle='--')
plt.ylabel(r'Change in length/$\Delta l$')
plt.xlabel(r'Temperature/$\theta$')
plt.title('A plot of change in length vs temperature')
#removing extra space
plt.tight_layout()
#saving the plot
plt.savefig('Plot1.png', dpi=800)
plt.legend()
plt.show()
