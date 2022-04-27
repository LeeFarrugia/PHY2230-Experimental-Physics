import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.integrate as integrate
 
# calling data from sheet
data = pd.read_excel('Experiment9Data.xlsx', 0)
datac = pd.read_excel('Experiment9CData.xlsx', 0)

# finding the average of the forbes bar readings
average_f = 0.25 * (data['F1'] + data['F2'] + data['F3'] + data['F4'])
# storing the x positions in a variable for later use
distance_x = (1/4) * (data['x1'] + data['x2'] + data['x3'] + data['x4'])
average_c = (1/3) * (datac['c1'] + datac['c2'] + datac['c3'])
time = (1/3) * (datac['t1'] + datac['t2'] + datac['t3'])
 
# finding the coefficients and co-variance matrix of theta(x)
coeffs, V = np.polyfit(distance_x, average_f, 2, cov=True)
# finding line of best fit
poly_function = np.poly1d(coeffs)
trendline = poly_function(distance_x)
 
# finding the coefficients and co-variance matrix of phi(t)
coeffsc, Vc = np.polyfit(time, average_c, 2, cov=True)
# finding line of best fit
poly_functionc = np.poly1d(coeffsc)
trendlinec = poly_functionc(time)
 
# finding the coefficients and co-variance matrix of t(phi)
coeffst, Vt = np.polyfit(average_c, time, 2, cov=True)
# finding the line of best fit
poly_functiont = np.poly1d(coeffst)
trendlinet = poly_functiont(average_c)
 
 
# defining a function to store the coefficients of theta(t)
def theta(a, b, c):
    return a, b, c
 
 
# function for squaring the coefficients of theta(t)
def theta2(a, b, c):
    return a**2, 2*a*b, 2*a*c, b**2, 2*b*c, c**2
 
 
# function for applying the coefficients of t(calibration) over the tuple
    from other function
def t(theta2, theta, a, b, c):
    x = tuple(map(a.__mul__, theta2))
    y = tuple(map(b.__mul__, theta))
    z = c
# returns a tuple with the combined coefficients 
    return x[0], x[1], x[2] + x[3] + y[0], x[4] + y[1], x[5] + y[2] + z
 
 
# function to apply the coefficient multiplication over tuple
    and returning new coefficients
def pdtheta(t, a, b):
    x = tuple(map((2*a).__mul__, t))
    return x[0], x[1], x[2], x[3], x[4]+b
 
 
# function to calculate the point for distance x with new coefficients 
def pdthetaplt(x, a, b, c, d, e):
    return a*np.power(x, 4) + b*np.power(x, 3) + c*np.power(x, 2) + d*x + e
 
# function to calculate the gradient
def gradient(x, a, b, c):
    return a*np.power(x, 2) + b*x + c
 
 
# calling function t with quadratic coefficients  in order 
    to do quadratic substitution
dtheta = (t(theta2(coeffs[0], coeffs[1], coeffs[2]), 
            theta(coeffs[0], coeffs[1], coeffs[2]), coeffst[0], coeffst[1],
            coeffst[2]))
# calling function in order to substitute x^4 equation into 
    partial derivative of theta/t
partial = (pdtheta(dtheta, coeffsc[0], coeffsc[1]))
# using coefficients from x^4 equation to calculate each point for distance_x
pd = pdthetaplt(distance_x, partial[0], partial[1], partial[2], 
                partial[3], partial[4])
 
# finding the coefficients and co-variance matrix of partial theta(x)
coeffspd, Vpd = np.polyfit(distance_x, pd, deg=2, cov=True)
# finding the line of best fit
poly_functionpd = np.poly1d(coeffspd)
trendlinepd = poly_functionpd(distance_x)
 
# numerically integrating straight part of graph
integration, errori = integrate.quad(poly_functionpd, 0.15, 0.25)
print(f'The integration is {integration} with an error of {errori}')
 
# obtaining the gradient of the straight part of graph
grad = (gradient(0.25, coeffs[0], coeffs[1], coeffs[2]) - gradient(0.15, 
        coeffs[0], coeffs[1], coeffs[2])) / (0.25 - 0.15)
print(f'The gradient is {grad}')
 
# obtaining the errors for the coefficients
error_average_f = np.sqrt(V[1][1]) + np.sqrt(V[0][0]) + np.sqrt(V[2][2])
error_average_c = np.sqrt(Vc[1][1]) + np.sqrt(Vc[0][0]) + np.sqrt(Vc[2][2])
error_average_pd = np.sqrt(Vpd[1][1]) + np.sqrt(Vpd[0][0]) + np.sqrt(Vpd[2][2])
 
# finding standard deviations of data sets
standard_deviation_f = np.std([data['F1'], data['F2'], data['F3'],
                                data['F4']], axis=0, ddof=1)
delta_f = 3.18 * standard_deviation_f / np.sqrt(4)
 
standard_deviation_c = np.std([datac['c1'], datac['c2'], datac['c3']],
                                axis=0, ddof=1)
delta_c = 4.30 * standard_deviation_c / np.sqrt(3)
 
standard_deviation_x = np.std([data['x1'], data['x2'], data['x3'],
                                data['x4']], axis=0, ddof=1)
delta_x = 3.18 * standard_deviation_x / np.sqrt(4)
 
standard_deviation_t = np.std([datac['t1'], datac['t2'], datac['t3']],
                                axis=0, ddof=1)
delta_t = 4.30 * standard_deviation_t / np.sqrt(3)
 
# defining plotting size, font, text thickness
plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"
f = plt.figure(figsize=(7.5, 10.5))
 
# plotting
plt.errorbar(distance_x, average_f, xerr=delta_x, yerr=delta_f,
             fmt='o', elinewidth=2, capthick=2, capsize=5,
             ecolor='grey')
plt.scatter(distance_x, average_f, label='Data Points')
plt.plot(distance_x, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.xlabel(r'$\mathrm{Distance}$ $x \mathrm{/cm}$')
plt.ylabel(r'$\mathrm{Temperature}$ $\theta \mathrm{/\degree C}$')
plt.title('Change in Temperature over Distance in Forbe\'s Bar')
plt.savefig('ThetavsXPlot.png', dpi=800)
 
plt.show()
 
f = plt.figure(figsize=(7.5, 10.5))
 
plt.errorbar(time, average_c, xerr=delta_t, yerr=delta_c,
             fmt='o', elinewidth=2, capthick=2, capsize=5,
             ecolor='grey')
plt.scatter(time, average_c, label='Data Points')
plt.plot(time, trendlinec, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.xlabel(r'$\mathrm{Time}$ $t \mathrm{/s}$')
plt.ylabel(r'$\mathrm{Temperature}$ $\phi \mathrm{/\degree C}$')
plt.title('Change in Temperature over Time in Calibration Bar')
plt.savefig('PhivsTPlot.png', dpi=800)
 
plt.show()
 
f = plt.figure(figsize=(7.5, 10.5))
 
plt.errorbar(average_c, time, xerr=delta_c, yerr=delta_t,
             fmt='o', elinewidth=2, capthick=2, capsize=5,
             ecolor='grey')
plt.scatter(average_c, time, label='Data Points')
plt.plot(trendlinec, time, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.ylabel(r'$\mathrm{Time}$ $t \mathrm{/s}$')
plt.xlabel(r'$\mathrm{Temperature}$ $\phi \mathrm{/\degree C}$')
plt.title('Change in Temperature over Time in Calibration Bar')
plt.savefig('TvsPhiPlot.png', dpi=800)
 
plt.show()
 
f = plt.figure(figsize=(7.5, 10.5))
 
plt.scatter(distance_x, pd, label='Data Points')
plt.plot(distance_x, trendlinepd, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.ylabel(r'$\frac{\partial \theta}{\partial t}$')
plt.xlabel(r'$\mathrm{Time}$ $t \mathrm{/s}$')
plt.title(r'$\frac{\partial \theta}{\partial t}$ against time')
plt.savefig('PartialPlot.png', dpi=800)
 
plt.show()
