import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np

data = pd.read_excel('Experiment 0.xlsx', 0)
average_v = 0.5 * (data['V1'] + data['V2'])
time = 0.5 * (data['t1'] + data['t2'])


def fit_ft(t, v0, t_c):
    return v0 * np.exp(-t/t_c)


popt, pcov = curve_fit(fit_ft, time, average_v, p0=(2,2))
fitted_line = fit_ft(time, popt[0], popt[1])

standard_deviation_V = np.std([data['V1'], data['V2']], axis=0, ddof=1)
delta_v = 12.7 * standard_deviation_V / np.sqrt(2)

standard_deviation_t = np.std([data['t1'], data['t2']], axis=0, ddof=1)
delta_t = 12.7 * standard_deviation_t / np.sqrt(2)

delta_v /= average_v
delta_t /= time

print(f'V0 is : {popt[0]}, with an error of: {(pcov[0][0])**0.5}')
print(f'T is : {popt[1]}, with an error of: {(pcov[1][1])**0.5}')

plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

f = plt.figure(figsize=(7.5, 10.5))
plt.errorbar(time, average_v, xerr=delta_t, yerr=delta_v, fmt='o', color='k', elinewidth=2, capthick=2,capsize=5, ecolor='grey')
plt.scatter(time, average_v, color='k', label='Data points')
plt.plot(time, fitted_line, 'b-', label='Fit')

plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')
plt.legend()
plt.xlabel(r"Time $\overline{t}/s$")
plt.ylabel(r"Voltage $\overline{V}/V$")
plt.title(r'A Plot of $\overline{V}/V$ vs $\overline{t}/s$')
plt.savefig('Experiment0ExpPlot.png', dpi=300)

plt.show()
