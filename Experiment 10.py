import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import *
from math import sqrt
 
# importing data from excel sheet and defining variables
data = pd.read_excel('Experiment10Data.xlsx', 1)
t2 = data['T^2']
l = data['l']
x_a = data['x_averages']
y_a = data['y_averages']
L = data['Lr'].mean()
h = data['h'].mean()
 
#finding the straight line equation of x vs y
coeffsm, covm = np.polyfit(x_a, y_a, 1, cov=True)
poly_funcm = np.poly1d(coeffsm)
trendlinem = poly_funcm(x_a)
 
#Finding the gradient and defining other variable
M = (coeffsm[0])
k = L / np.sqrt(12)
print(f'The mass ratio is {coeffsm[0]}')
 
# finding the error for the values of x and y for error bars
stdx = [np.std(data['x1'].dropna(), axis=0, ddof=1), 
        np.std(data['x2'].dropna(), axis=0, ddof=1),
        np.std(data['x3'].dropna(), axis=0, ddof=1), 
        np.std(data['x4'].dropna(), axis=0, ddof=1),
        np.std(data['x5'].dropna(), axis=0, ddof=1)]
deltax = tuple(map((4.30 / np.sqrt(3)).__mul__, stdx))
 
stdy = [np.std(data['y1'].dropna(), axis=0, ddof=1), 
        np.std(data['y2'].dropna(), axis=0, ddof=1),
        np.std(data['y3'].dropna(), axis=0, ddof=1), 
        np.std(data['y4'].dropna(), axis=0, ddof=1),
        np.std(data['y5'].dropna(), axis=0, ddof=1)]
deltay = tuple(map((4.30 / np.sqrt(3)).__mul__, stdy))
 
# finding error of m/M gradient
deltaM = np.sqrt(covm[0][0])
print(f'The error for m/M is {deltaM}')
 
# fiding error of other constants
deltah = np.std([data['h'].dropna()]) / data['h'].mean()
deltak = np.std([data['Lr'].dropna()]) / (data['Lr'].mean() * np.sqrt(12))
deltal = np.std([data['l'].dropna()]) / data['l'].mean()
deltat2 = np.std([data['T^2'].dropna()]) / data['T^2'].mean()
 
# defining the function for l_0
def xplotfunction(x):
    return (M * ((h ** 2) + (k ** 2)) + (x ** 2)) / ((M * h) + x)
 
# plugging in values for l to plot
xp = xplotfunction(l)
 
# defining a function for the partial derivation of l_0
def derivative(e, f, g, p):
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    d = Symbol('d')
    equation = (a*(b ** 2 + c ** 2) + d ** 2) / (a * b + d)
    diff_a = Derivative(equation, a)
    diff_b = Derivative(equation, b)
    diff_c = Derivative(equation, c)
    diff_d = Derivative(equation, d)
    da = diff_a.doit()
    db = diff_b.doit()
    dc = diff_c.doit()
    dd = diff_d.doit()
    dM = da.subs({a: e, b: f, c: g, d: p}).evalf()
    dh = db.subs({a: e, b: f, c: g, d: p}).evalf()
    dk = dc.subs({a: e, b: f, c: g, d: p}).evalf()
    dl = dd.subs({a: e, b: f, c: g, d: p}).evalf()
    return ((np.power(dM, 2))*deltaM + (np.power(dh, 2))*deltah +     
            (np.power(dk, 2))*deltak + (np.power(dl, 2))*deltal)
 
 
# calculating the combined error of l_0
xerr= (sqrt(derivative(M, h, k, l[0])), sqrt(derivative(M, h, k, l[1])), 
sqrt(derivative(M, h, k, l[2])), sqrt(derivative(M, h, k, l[3])), 
sqrt(derivative(M, h, k, l[4])))
 
# finding the straight line equation of T^2 vs l_0 and gradient
coeffs, cov = np.polyfit(xp, t2, 1, cov=True)
poly_func = np.poly1d(coeffs)
trendline = poly_func(xp)
print(f'The gradient of T^2 vs x is {coeffs[0]}')
 
# fidning gravity and its error
gravity = (4 * (np.pi ** 2)) / (coeffs[0])
print(f'Gravity is {gravity}')
deltagrav = (4 * np.pi ** 2) / gravity ** 2
print(f'The error of the gravity is {deltagrav}')
 
# defining the fonts and sizes to be used
plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
 
f = plt.figure(figsize=(7.3, 10.7))
 
# plotting the error bars, data points, fitted line and axis, title are defined
plt.errorbar(x_a, y_a, xerr=deltax, yerr=deltay, fmt='o', color='k', elinewidth=2, 
            capthick=2, capsize=5, ecolor='grey')
plt.scatter(x_a, y_a, color='k', label='Data Points')
plt.plot(x_a, trendlinem, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.xlabel(r'$x \mathrm{/m}$')
plt.ylabel(r'$y \mathrm{/m}$')
plt.title('x-distance vs y-distance')
plt.savefig('mMgraph.png', dpi=800)
plt.show()
