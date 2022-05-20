import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read excel file using pandas
data = pd.read_excel('jfet_data.xlsx', 0)

average_V = 0.5 * (data['V1'] + data['V2'])
current = average_V / data['R']

def fit_func(v_s, v_t, k, a):
    return k * (np.power(v_t - v_s, a))

# First argument is the function we want to fit
# Second argument is the x_data (in this case current)
# Third argument is the y_data (in this case average_V)
popt, pcov = curve_fit(fit_func, average_V, current, p0=(2.5, 1, 1))

print(f'value of V_t is {popt[0]:.2f}')
print(f'value of k is {popt[1]:.2f}')
print(f'value of a is {popt[2]:.2f}')

fitted_line = fit_func(average_V, popt[0], popt[1], popt[2])

plt.rcParams["font.family"] = "Cambria"
plt.rcParams["font.size"] = 12
plt.rcParams["font.weight"] = "normal"

f = plt.figure(figsize=(8, 10))

plt.scatter(current, average_V, color='k')
plt.plot(fitted_line, average_V, 'k--')

plt.minorticks_on()
plt.grid(b=True, which='major', linestyle='-')
plt.grid(b=True, which='minor', linestyle='--')

plt.xlabel(r"$I_d$")
plt.ylabel(r"$V_S$")

plt.show()