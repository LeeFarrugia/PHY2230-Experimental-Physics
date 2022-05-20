import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_excel('Experiment 0.xlsx', 0)       # calling the excel file for the data
average_v = 0.5 * (data['V1'] + data['V2'])        # finding the average of each column of voltage
time = 0.5 * (data['t1'] + data['t2'])             # finding the average of each column of time

lnV = np.log(average_v)                            # finding the log of the average voltage

coeffs, V = np.polyfit(time, lnV, 1, cov=True)     # using polyfit in order to obtain m and c and covariance
vf = np.exp(coeffs[1])                             # using c to find V0
Tf = (np.power(coeffs[0], -1)) * -1                # using m to frind T

error_vf = np.sqrt(V[1][1])                        # calling the position in the covariance matrix as the error value of V0
error_Tf = np.sqrt(V[0][0])                        # calling the position in the covariance matrix as the error value of T

print(f'lnV is: {vf}, with an error of: {error_vf}')    # displaying V0 with error
print(f'T is: {Tf}, with an error of: {error_Tf}')      # displaying T with error

standard_deviation_V = np.std([data['V1'], data['V2']], axis=0, ddof=1)      # finding the std of V
delta_v = 12.7 * standard_deviation_V / np.sqrt(2)                           # finding the change in V wrt pop

standard_deviation_t = np.std([data['t1'], data['t2']], axis=0, ddof=1)     # finding the std of t
delta_t = 12.7 * standard_deviation_t / np.sqrt(2)                          # finding the change in t wrt pop

delta_v /= average_v                               # updating the change in V
delta_t /= time                                    # updating the change in t

poly_function = np.poly1d(coeffs)                  # using the gradient and y-intercept to calculate the best straight line
trendline = poly_function(time)

plt.rcParams["font.family"] = "Cambria"            # defining the font to be used
plt.rcParams["font.size"] = 12                     # defining the font size
plt.rcParams["font.weight"] = "normal"             # defining the thickness of the font

f = plt.figure(figsize=(7.5, 10.5))                # defining the size of the figure
plt.errorbar(time, lnV, xerr=delta_t, yerr=delta_v, fmt='o', color='k', elinewidth=2, capthick=2,capsize=5,
             ecolor='grey')                        # plotting the error bars of each point
plt.scatter(time, lnV, color='k', label='Data Points')      # plotting the scatter graph
plt.plot(time, trendline, color='b', label='Fit')        # plotting the line

plt.minorticks_on()                                # turning on the minor lines
plt.grid(b=True, which='major', linestyle='-')     # defining the style for major line
plt.grid(b=True, which='minor', linestyle='--')    # defining the style for minor lines
plt.legend()                                       # displaying the legend
plt.xlabel(r"Time $\overline{t}/s$")                          # defining the x-axis label
plt.ylabel(r"ln Voltage $ln(\overline{V})$")                  # defining the y-axis label
plt.title(r'A Plot of $ln(\overline{V})$ vs $\overline{t}/s$')                  # defining the graph title
plt.savefig('Experiment0LinearPlot.png', dpi=300)      # saving the figure

plt.show()                                         # showing the plotted graph