# -*- coding: utf-8 -*-
"""
  Enthalpie : trace l'enthalpie libre de Landau et l'aimantation
"""

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib 

plt.rcParams.update({'font.size': 22})

# enthalpie
def enthalpie (a, b, M):
    return a*M**2 + b*M**4

# aimantation
def aimantation (s, a, b, Tc, T):
    return s * np.sqrt (a / b * (Tc - T))

# tracé de l'enthalpie
m = np.linspace (-2, 2, 1000)
plt.figure (figsize = (20, 10))
plt.plot (m, enthalpie (-3, 1, m), linewidth = 5)
plt.plot (m, enthalpie (0.25, 0.25, m), linewidth = 5)
plt.xlabel ("$M / M_{max}$")
plt.ylabel ("$G / kT$")
plt.title ("$G(M) = aM^2 + bM^4$")
plt.legend(['$a < 0, b > 0$', '$a > 0, b > 0$'], loc=1)
plt.show ()

# tracé de l'enthalpie avec un champ B
B = 4
m = np.linspace (-2, 2, 1000)
plt.figure (figsize = (20, 10))
plt.plot (m, enthalpie (-3, 1, m) + 2*m, linewidth = 5)
plt.xlabel ("$M / M_{max}$")
plt.ylabel ("$G / kT$")
plt.title ("$G(M) = aM^2 + bM^4 - BM$")
plt.show ()

# tracé de l'aimantation
Tc = 50
a = 1
b = Tc
T = np.linspace (0, Tc, 1000)
plt.figure (figsize = (20, 10))
plt.plot (T/Tc, aimantation (1, a, b, Tc, T), linewidth = 5)
plt.hlines (0, 0, 1, color='black', linewidth=3)
plt.hlines (0, 1, 1.5, linewidth=5)
plt.ylabel ("$M / M_{max}$")
plt.xlabel ("$T/T_c$")
plt.title ("$M(T)$")
plt.show ()