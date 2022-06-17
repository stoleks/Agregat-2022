# -*- coding: utf-8 -*-
"""
  Trace les modes de vibration d'une corde
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# n : ordre
# c : célérité
# L : longueur de la corde
def modePropre (x, t, n, c, L):
    k = np.pi * n / L
    return np.cos (k * c * t) * np.sin (k * x)

# propriété de l'onde
c = 500
L = 1

# propriété de la figure
fig = plt.figure ()
# plt.rcParams.update({'font.size': 22})
#plt.figure (figsize = (20, 10)) # cette commande ne marche pas avec l'animation
plt.xlabel ("$x / L$")
plt.ylabel ("$y(x, t) / y_{max}$")
plt.title ("Troisième mode propre d'une corde")

# tracé des 4 premiers modes
x = np.linspace (0, L, 1000)
plt.plot (x / L, modePropre (x, 0, 3, c, L), label=r"y_3(x, 0)", linewidth=5)
# plt.plot (x / L, modePropre (x, 0, 1, c, L), linewidth=5)
# plt.plot (x / L, modePropre (x, 0, 2, c, L), linewidth=5)
# plt.plot (x / L, modePropre (x, 0, 4, c, L), linewidth=5)
# plt.legend (['$y_1 (x, 0)$', '$y_2 (x, 0)$', '$y_3 (x, 0)$', '$y_4 (x, 0)$'], loc=3)
plt.axhline (y=0, color='black')


"""
animation du troisieme mode
"""
# calcul du mode
t = 0
images = 1200
tempsMax = 2/c
dt = tempsMax / images
onde = np.zeros ((images, len (x)))
for i in range(images):
    onde[i, :] = modePropre (x, t, 3, c, L)
    t += dt

# animation
line, = plt.plot ([], [], 'darkorange', label=r"$y_3 (x, t)$", linewidth=2)
def animate (i):
    line.set_data (x, onde[i, :])
    return line,
plt.legend (loc=3)
anim = animation.FuncAnimation (fig, animate, frames=images, interval=1, blit=True, repeat=True)

plt.show ()