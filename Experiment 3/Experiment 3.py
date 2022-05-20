import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# importing data from excel
data = pd.read_excel('Experiment 3.xlsx', 0)
# defining V, I, T from data
V = data['voltage']
I = (1/3) * (data['c1'] + data['c2'] + data['c3'])
Ts = data['tempc'].mean() + 273.15
# defining constants
h = 6.6e-34
c = 3e8
k = 1.38e-23
N = 1

# finding the line equation of V vs I
coeffs, cov1 = np.polyfit(V, I, 1, cov=True)
polyfunc = np.poly1d(coeffs)
# creating the line of best fit for the data
trendline = polyfunc(V)

# finding the error for each point
dV = 0.01
dI = 4.30 * (np.std([data['c1'], data['c2'], data['c3']], 
             axis=0, ddof=1)/(np.sqrt(3)))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.errorbar(V, I, xerr=dV, yerr=dI, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel('V/V')
plt.ylabel('I/A')
plt.title('V/V vs I/A')
plt.legend()
plt.show()

# defining the point to be used, the linear part
V2 = V[20:]
# defining an array to plot from 0
Vp = np.linspace(0, 5.05, 100)
I2 = I[20:]

coeffsv, covv = np.polyfit(V2, I2, 1, cov=True)
plofuncv = np.poly1d(coeffsv)
trendlinev = polyfunc(V2)

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining plot parameters
plt.minorticks_on()
plt.errorbar(V2, I2, xerr=dV, yerr=dI2, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.plot(V2, trendlinev, color='k', label='Fit')
plt.xlabel('V/V')
plt.ylabel('I/A')
plt.title('I/A vs V/V')
plt.savefig('VvsI2.png', dpi=800)
plt.legend()
plt.show()

# finding R at each point
R = V2/I2

# finding the error of each point
dI2 = dI[20:]
dR = R * (np.sqrt(((dV/V2)**2)+((dI2/I2)**2)))

# finding the equation of the straight line
coeffs2, cov2 = np.polyfit(I2, R, 1, cov=True)
polyfunc2 = np.poly1d(coeffs2)
# defining the line of best fit
trendline2 = polyfunc2(Vp)
# defining the resistance at the start
Rs = coeffs2[1]
Rprecision = (dRs/Rs) * 100
print(f'The resistance is {Rs:.2f} with an error of 
        {dRs:.2f}, and a precision of {Rprecision:.2f}%')

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.errorbar(I2, R, xerr=dI2, yerr=dR, fmt='o', color='k', 
             elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.plot(Vp, trendline2, color='k', label='Fit')
plt.xlabel('I/A')
plt.xlim(0)
plt.ylim(0)
plt.ylabel(r'R/$\Omega$')
plt.title(r'R/$\Omega$ vs I/A')
plt.legend()
plt.show()

# finding the power, lnP and lnR of each point
P = V2*I2
lnP = np.log(P)
lnR = np.log(R)
lnRp = np.linspace(0, 2, 100)
# defining the maximum power
Pmax = np.max(P)

# finding the equation of the straight line
coeffs3, cov3 = np.polyfit(lnR, lnP, 1, cov=True)
polyfunc3 = np.poly1d(coeffs3)
# defining the line of best fit
trendline3 = polyfunc3(lnRp)

# finding the value of m from the gradient
m = coeffs3[0]/4
merr = np.sqrt((cov3[0][0])/4)
mprecision = (merr/m) * 100
print(f'The value of m is {m:.2f}, with and error of 
        {merr:.2f}, and a precision of {mprecision:.2f}%')

# finding the error of each point
dlnR = (np.sqrt(((dV/V2)**2)+((dI2/I2)**2)))
dlnP = (np.sqrt(((dV/V2)**2)+((dI2/I2)**2)))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.errorbar(lnR, lnP, xerr=dlnR, yerr=dlnP, fmt='o',
             color='k', elinewidth=2, capthick=2, capsize=5,
             ecolor='grey', label='Data Points')
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.plot(lnRp, trendline3, color='k', label='Fit')
plt.xlabel(r'$\ln{\mathrm{R}}$')
plt.ylabel(r'$\ln{\mathrm{P}}$')
plt.title(r'$\ln{\mathrm{R}}$ vs $\ln{\mathrm{P}}$')
plt.legend()
plt.show()

# finding the temperature at each point of the resistance
T = np.max(Ts*((R/Rs)**m))
print(f'The maximum temperature is {T:.2f} K')

# defining the whole range of the spectrum
wl1 = np.linspace(200, 9200, 500) * 1e-9
# defining the p(lambda) at each point
Plamb = N/((wl1**5)*(np.exp((h*c)/(wl1*k*T))-1))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$\lambda$/nm')
plt.ylabel(r'$p(\lambda)$')
plt.title(r'$p(\lambda)$ vs $\lambda$ with N=1')
plt.plot(wl1, Plamb, 'k--')
plt.show()

# finding the area under the graph with N=1
trapezium1 = np.trapz(Plamb, wl1)
print(f'The total power is {trapezium1} W, 
      the power at 15V is {Pmax:.2f} W')

# changing the value of N to the accurate one
N = np.max(P)/trapezium1
# defining the p(lambda) at each point
Plamb = N/((wl1**5)*(np.exp((h*c)/(wl1*k*T))-1))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$\lambda$/nm')
plt.ylabel(r'$p(\lambda)$')
plt.title(r'$p(\lambda)$ vs $\lambda$ with proper N')
plt.plot(wl1, Plamb, 'k--')
plt.show()

# finding the area under the graph with the proper N
trapezium2 = np.trapz(Plamb, wl1)
print(f'The total power is {trapezium2:.2f} W, 
      the power at 15V is {Pmax:.2f} W')

# defining the visible light spectrum
wl2 = np.linspace(400, 700, 500) * 1e-9
# defining the p(lambda) at each point
Plight = N/((wl2**5)*(np.exp((h*c)/(wl2*k*T))-1))

# defining the font
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the figure size
f = plt.figure(figsize=(7.3, 10.7))

# defining plot parameters
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.plot(wl2, Plight, 'k--')
plt.show()

# finding the area under the graph of the visible light part
trapezium3 = np.trapz(Plight, wl2)
print(f'The useful total power is {trapezium3:.2f} W')

# finding the efficiency
powratio = (trapezium3/np.max(P))*100
print(f'The light efficiency is {powratio:.4f}%')
