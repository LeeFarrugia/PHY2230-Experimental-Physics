import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing data from excel and defining constants
data = pd.read_excel('Experiment 15.xlsx')
svr = data['svred'].mean()
svo = data['svorange'].mean()
svy = data['svyellow'].mean()
svg = data['svgreen'].mean()
svb = data['svblue'].mean()

wavelengths = data['wavelength']
c = 3e8
e = -1.6e-19

energy = np.array([(svr*e), (svo*e), (svy*e), (svg*e), (svb*e)])
frequency = np.array([(c/wavelengths[0]), (c/wavelengths[1]), 
                      (c/wavelengths[2]), (c/wavelengths[3]), 
                      (c/wavelengths[4])])

# finding the change in the stopping voltage
svstd = np.array([np.std(data['svred']), np.std(data['svorange']), 
                  np.std(data['svyellow']), np.std(data['svgreen']), 
                  np.std(data['svblue'])])
deltasv = np.absolute(e * 2.78 * svstd/np.sqrt(5))

# finding the coefficients and line of best fit
coeffs, cov = np.polyfit(frequency, energy, 1, cov=True)
polyfunc = np.poly1d(coeffs)
trendline = polyfunc(frequency)

# finding the required values and the errors
m = coeffs[0]
yint = coeffs[1]
merr = np.sqrt(cov[0][0])
yinterr = np.sqrt(cov[1][1])

# finding the accuracy and precision
maccuracy = np.absolute(((m/6.62e-34)-1) * 100)
mprecision = (merr/m) * 100
yintprecision = np.absolute((yinterr/yint) * 100)

# printing everything
print(f'Planks constant was found to be: {m}, 
        with and error of {merr}. '
      f'Its accuracy is {maccuracy:.2f}%, 
        and with a precision of {mprecision:.2f}%')
print(f'The work function of the material was 
        found to be {yint}, with an error of {yinterr}. '
      f'Its precision is {yintprecision}%')

# defining the fonts and sizes to be used
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 12
plt.rcParams['font.weight'] = 'normal'

# defining the plot size
f = plt.figure(figsize=(7.3, 10.7))

plt.errorbar(frequency, energy, xerr=0.01, yerr= deltasv, 
             fmt='o', color='k', elinewidth=2, 
             capthick=2, capsize=5, ecolor='grey', 
             label='Data Points')
plt.plot(frequency, trendline, color='k', label='Fit')
plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.xlabel(r'$F$/Hz')
plt.ylabel(r'$KE_{\mathrm{max}}$/J')
plt.title(r'$KE_{\mathrm{max}}$/J vs $F$/Hz')
plt.legend()
plt.savefig('KEvsFgraph.png', dpi=800)
plt.show()
