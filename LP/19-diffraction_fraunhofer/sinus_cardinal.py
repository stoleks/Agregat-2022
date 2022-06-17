# -*- coding: utf-8 -*-
"""
  Trace sinc et sinc^2
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams.update({'font.size': 16})


# sinus cardinal
def sinc (x):
    return np.sin (x) / x

# trace les axes du diagrammes sinc
def traceAxes (axes):
    # place l'origine des axes en (0, 0)
    axes.spines[["left", "bottom"]].set_position(("data", 0))
    # cache les informations inutiles
    axes.spines[["top", "right"]].set_visible(False)

    # dessine l'axe x et y
    axes.plot (1, 0, ">k", transform = axes.get_yaxis_transform(), clip_on=False, linewidth=5)
    axes.plot (0, 1, "^k", transform = axes.get_xaxis_transform(), clip_on=False, linewidth=5)
    axes.set_xlabel("$x / x_0$", loc="right", fontsize=18)


# paramètre oscillation
a = 0.01
f = 0.2
lambd = 600e-9
xMax = 9.4
x = np.linspace (-xMax, xMax, 10000)

# tracé de sinc
fig, axes = plt.subplots(figsize = (16, 8))
traceAxes (axes)
axes.plot (x/9.4, sinc (x), linewidth = 5)
plt.title ("Amplitude")
axes.set_ylabel("$A / A_0$", loc="top", fontsize=18)
plt.show ()

# tracé de sinc^2
fig, axes = plt.subplots(figsize = (16, 8))
traceAxes (axes)
axes.plot (x/9.4, (sinc (x))**2, linewidth = 5)
plt.title ("Intensité")
axes.set_ylabel("$I / I_0$", loc="top", fontsize=18)
plt.show ()