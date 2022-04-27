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
