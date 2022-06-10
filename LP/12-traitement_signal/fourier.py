# -*- coding: utf-8 -*-
"""
  Fourier : trace la série de fourier d'un signal carré
"""

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib 

plt.rcParams.update({'font.size': 22})

# enthalpie
def carreFourier (N, omega, t):
    total = 0
    for p in range(0, N):
        n = 2*p + 1
        total = total + np.sin (n * omega * t) / n
    return 4 * total / np.pi

# tracé de la série de Fourier
f = 50
T = 1 / f
omega = 2*np.pi*f
t = np.linspace (-T, T, 1000)
plt.figure (figsize = (20, 10))
plt.plot (t/T, carreFourier (1, omega, t), linewidth = 5)
plt.plot (t/T, carreFourier (10, omega, t), linewidth = 5)
plt.plot (t/T, carreFourier (100, omega, t), linewidth = 5)
plt.plot (t/T, carreFourier (10000, omega, t), linewidth = 5)
plt.xlabel ("$t/ T$")
plt.ylabel ("$s$")
plt.title ("$s(t)$")
plt.show ()