# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib 

plt.rcParams.update({'font.size': 22})

# vecteur d'onde
def vecteurOnde (longueurOnde):
    return 2 * np.pi / longueurOnde

# transmission T du Fabry-Perot
def transmission (R, d, theta, lambd):
    k = vecteurOnde (lambd)
    cos = np.cos (2 * d * k *np.cos (theta))
    return (1 - R)**2 / (1 + R**2 - 2*R*cos)


## cavité de taille variable
# paramètres de l'onde
lOnde = 600e-9

# tracé de T(d)
d = np.linspace (0.25, 2.25, 10000)
plt.figure (figsize = (20, 10))
plt.plot (d, transmission (0.2, d*lOnde, 0, lOnde), linewidth=5)
plt.plot (d, transmission (0.8, d*lOnde, 0, lOnde), linewidth=5)
plt.plot (d, transmission (0.95, d*lOnde, 0, lOnde), linewidth=5)
plt.xlabel ("Taille de la cavité $m \lambda$")
plt.ylabel ("Transmission $T_{FP}$")
plt.title ("$T_{FP}$ en fonction de la taille de la cavité")
plt.legend(['R = 0.2', 'R = 0.8', 'R = 0.99'], loc=4)
plt.show ()

# tracé de T(lambda)
lOndes = np.linspace (5895.924, 5889.950, 10000)
plt.figure (figsize = (20, 10))
plt.plot (lOndes, transmission (0.9, 1e-3, 0, lOndes/10**10), linewidth=5)
plt.xlabel ("$\lambda$ [nm]")
plt.ylabel ("Transmission $T_{FP}$")
plt.title ("$T_{FP}$ en fonction de $\lambda$")
plt.show ()