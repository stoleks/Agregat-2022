# -*- coding: utf-8 -*-
"""
  Resonance : trace la norme des fonctions de transfert
  en position et vitesse pour 5 valeurs de Q
"""

import matplotlib.animation as animation
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import matplotlib 

plt.rcParams.update({'font.size': 22})

# norme fonction de transfert position
def Hv (omega, omega0, Q):
    den = 1 + Q**2 * (omega / omega0 - omega0/omega)**2
    return Q / (omega0 * np.sqrt (den))


# norme fonction de transfert vitesse
def Hx (omega, omega0, Q):
    den = (omega/omega0)**2 + Q**2 * (1 - (omega/omega0)**2)**2
    return Q / (omega0**2 * np.sqrt (den))

## paramètre resonance
Q = [0.3, 0.7, 1, 2, 4]
omega0 = 1
omega = np.linspace (0, 5, 100000)

# tracé de H_x
plt.figure (figsize = (20, 10))
for q in Q:
    plt.plot (omega, Hx (omega, omega0, q), linewidth=5)
plt.axvline (x=omega0, color='red', linestyle='--', linewidth=4)
plt.legend (['Q = 0.3', 'Q = 0.7', 'Q = 1', 'Q = 2', 'Q = 4'], loc=1)
plt.xlabel ("$\omega / \omega_0$")
plt.ylabel ("$H_x$ [$s^2$]")
plt.title ("$H_x (\omega)$")
plt.show ()

# tracé de H_v
plt.figure (figsize = (20, 10))
for q in Q:
    plt.plot (omega, Hv (omega, omega0, q), linewidth=5)
plt.axvline (x=omega0, color='red', linestyle='--', linewidth=4)
plt.legend (['Q = 0.3', 'Q = 0.7', 'Q = 1', 'Q = 2', 'Q = 4'], loc=1)
plt.xlabel ("$\omega / \omega_0$")
plt.ylabel ("$H_v$ [$s$]")
plt.title ("$H_v (\omega)$")
plt.show ()