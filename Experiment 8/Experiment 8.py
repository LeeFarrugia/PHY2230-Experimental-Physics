import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import *
from math import sqrt

# inputting data from excel sheet
data = pd.read_excel('Experiment 8.xlsx')
# converting all angles into radians
apexA = np.deg2rad(data['apexA'])
apexAp = np.deg2rad(data['apexAp'])
apexB = np.deg2rad(data['apexB'])
apexBp = np.deg2rad(data['apexBp'])
# working out the apex angle
alpha = ((np.absolute(apexA-apexAp)/2)+(np.absolute(apexB-apexBp)/2))/2

# defining minimum readability and actual values
dA = 1/120
dB = 1/120
A = 1.5220
B = 4.59e-15

# finding the 1/wavelength**2 values
xRed = 1/(6.438e-7)**2
xGreen = 1/(5.086e-7)**2
xCyan = 1/(4.80e-7)**2
xBlue = 1/(4.678e-7)**2

# finding the minimum deviance angle of all colours
RedA = np.absolute(np.deg2rad(data['redA']-data['redAp']))/2
RedB = np.absolute(np.deg2rad(data['redB']-data['redBp']))/2
devRed = (RedA+RedB)/4

GreenA = np.absolute(np.deg2rad(data['greenA']-data['greenAp']))/2
GreenB = np.absolute(np.deg2rad(data['greenB']-data['greenBp']))/2
devGreen = (GreenA+GreenB)/4

CyanA = np.absolute(np.deg2rad(data['cyanA']-data['cyanAp']))/2
CyanB = np.absolute(np.deg2rad(data['cyanB']-data['cyanBp']))/2
devCyan = (CyanA+CyanB)/4

BlueA = np.absolute(np.deg2rad(data['blueA']-data['blueAp']))/2
BlueB = np.absolute(np.deg2rad(data['blueB']-data['blueBp']))/2
devBlue = (BlueA+BlueB)/4

nRed = np.sin((alpha + devRed)/2)/np.sin(alpha/2)
nGreen = np.sin((alpha + devGreen)/2)/np.sin(alpha/2)
nCyan = np.sin((alpha + devCyan)/2)/np.sin(alpha/2)
nBlue = np.sin((alpha + devBlue)/2)/np.sin(alpha/2)

# defining the y-axis and x-axis arrays
Y = np.hstack([nRed, nGreen, nCyan, nBlue])
X = np.array([xRed, xGreen, xCyan, xBlue])

# defining the partial derivative function for errors
def terror(c, d, dA):
    a = Symbol('a')
    b = Symbol('b')
    equation = ((a-b)/2)
    diffa = Derivative(equation, a)
    diffb = Derivative(equation, b)
    da = diffa.doit()
    db = diffb.doit()
    dc = da.subs({a: c, b: d}).evalf()
    dd = db.subs({a: c, b: d}).evalf()
    return sqrt((dc * dA) ** 2 + (dd * dA) ** 2)

def aerror(e, f, dapexA, dapexB):
    a = Symbol('a')
    b = Symbol('b')
    equation = ((a+b)/2)
    diffa = Derivative(equation, a)
    diffb = Derivative(equation, b)
    da = diffa.doit()
    db = diffb.doit()
    de = da.subs({a: e, b: f}).evalf()
    df = db.subs({a: e, b: f}).evalf()
    return sqrt((de * dapexA) ** 2 + (df * dapexB) ** 2)

def nerror(g, h, err, err2):
    a = Symbol('a')
    b = Symbol('b')
    equation = (sin((a+b)/2))/(sin(a/2))
    diffa = Derivative(equation, a)
    diffb = Derivative(equation,b)
    da = diffa.doit()
    db = diffb.doit()
    dg = da.subs({a : g, b : h}).evalf()
    dh = db.subs({a : g, b : h}).evalf()
    return sqrt((dg * err) ** 2 + (dh * err2) ** 2)

def verror(i, h, err, err2):
    a = Symbol('a')
    b = Symbol('b')
    equation = (a+b)/4
    diffa = Derivative(equation, a)
    diffb = Derivative(equation, b)
    da = diffa.doit()
    db = diffb.doit()
    di = da.subs({a : i, b : h}).evalf()
    dh = db.subs({a : i, b : h}).evalf()
    return sqrt((di * err) ** 2 + (dh * err2) ** 2)

# finding the errors for y-axis and x-axis values
dapexA = terror(apexA, apexAp, dA)
dapexB = terror(apexB, apexBp, dB)
dalpha = aerror(dapexA, dapexB, dapexA, dapexB)

vred = verror(RedA, RedB, dA, dB)
vgreen = verror(GreenA, GreenB, dA, dB)
vcyan = verror(CyanA, CyanB, dA, dB)
vblue = verror(BlueA, BlueB, dA, dB)

dnred = nerror(alpha,devRed,dalpha,vred)
dngreen = nerror(alpha,devGreen,dalpha,vgreen)
dncyan = nerror(alpha,devCyan,dalpha,vcyan)
dnblue = nerror(alpha,devBlue,dalpha,vblue)

# defining the error array for the y-axis
deltaY = np.hstack([dnred, dngreen, dncyan, dnblue])

# finding the line of best for the data gathered
coeffs, cov = np.polyfit(X, Y, deg=1, cov=True)
polyfunct = np.poly1d(coeffs)
trendline = polyfunct(X)

# finding the error for the coefficients
aerr = np.sqrt(cov[1][1])
berr = np.sqrt(cov[0][0])

# finding the accuracy for each coefficient
accuracyA = (coeffs[1]/A)*100
accuracyB = ((coeffs[0]/B)-1)*100
precisionA = (aerr/coeffs[1])*100
precisionB = (berr/coeffs[0])*100

# printing out the required information
print(f'A is found to be: {coeffs[1]:.2f} 
        with an error of: {aerr:.2e}')
print(f'A has an accuracy of: {accuracyA:.2f}% 
        and a precision of: {precisionA:.2f}%')
print(f'B is found to be: {coeffs[0]:.2e} 
        with an error of: {berr:.2e}')
print(f'B had an accuracy of: {accuracyB:.2f}% 
        and a precision of: {precisionB:.2f}%')

# defining the fonts and sizes to be used
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
plt.figure(figsize=(7.3, 10.7))

# plotting the figure
plt.errorbar(X, Y, xerr=0, yerr=deltaY, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.plot(X, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(visible=True, which='major', linestyle='-')
plt.grid(visible=True, which='minor', linestyle='--')
plt.title(r'A graph of $n(\lambda)$ vs $\frac{1}{\lambda^2}$')
plt.ylabel(r'$n(\lambda)$')
plt.xlabel(r'$\frac{1}{\lambda^2}$/$\frac{1}{m^{-2}}$')
# removing excess space from figure
plt.tight_layout()
plt.savefig('Plot1.png', dpi=800)
plt.legend()
plt.show()
