import matplotlib.pyplot as plt
import numpy as np

vals = np.linspace(0, 4*np.pi, 100)
x = np.sin(vals)
y = np.cos(vals)

plt.plot(vals,x)
plt.plot(vals,y)
plt.title('Sine and Cosine curves')
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.legend()
plt.show()