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

# vitesse de la lumière
c = 299792458

# norme fonction de transfert position
def gamma (v):
    beta = v / c
    return 1 / np.sqrt (1 - beta**2)

# tracé de gamma (v)
v = np.linspace (0, 0.95*c, 1000)
plt.figure (figsize = (20, 10))
plt.plot (v/c, gamma(v), linewidth = 5)
#plt.hlines (1.5, 0, 1, color='red', linestyle='--', linewidth=3)
plt.xlabel ("$v / c$")
plt.ylabel ("$\gamma$")
plt.title ("$\gamma (v) = 1 / \sqrt{1 - v^2/c^2}$")
plt.show ()