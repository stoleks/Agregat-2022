# -*- coding: utf-8 -*-
"""
Trace les premières fonctions d'onde d'un atome hydrogénoïde
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm, colors
import scipy.special as spe
from scipy.integrate import odeint

#
def densiteRadiale (r, n, l):
    N = n - l - 1
    r0 = 2*r / n
    coeff = np.sqrt ((2/n)**3 * spe.factorial(N) / (2*n * spe.factorial(n + l)))
    laguerre = spe.assoc_laguerre (r0, N, 2*l + 1)
    return coeff * np.exp (-r/n) * (r0)**l * laguerre

#
def harmoniqueSpherique (phi, theta, l, m):
    return spe.sph_harm (m, l, phi, theta).real

#
def ondeHydrogene(r, phi, theta, n, l, m):
    return densiteRadiale (r, n, l) * harmoniqueSpherique (phi, theta, l, m)


# trace la densité de présence selon le plan y
def traceDensitePresence (n, l, m, limite = 50):
    # definit l'espace de tracé
    x1d = np.linspace (-limite, limite, 500)
    z1d = np.linspace (-limite, limite, 500)
    x, z = np.meshgrid (x1d, z1d)
    y   = 0

    # calcule les coordonnées sphériques
    r     = np.sqrt (x**2 + y**2 + z**2)
    theta = np.arctan2 (np.sqrt(x**2+y**2), z)
    phi   = np.arctan2 (y, x)
    # calcule la densité de présence
    psi = 4*np.pi * r**2 * ondeHydrogene (r, phi, theta, n, l, m)**2

    # trace la densité de présence en coordonnée sphérique
    plt.figure (figsize = (20, 16))
    plt.contourf (x, z, psi, 20, cmap='seismic', alpha=0.6)
    plt.colorbar ()
    # légende du graphe
    plt.title (f"$4\pi r^2 |\psi|^2, \; n,l,m={n,l,m}$", fontsize=20)
    plt.xlabel ('X', fontsize=20)
    plt.ylabel ('Y', fontsize=20)


# trace les harmonique sphérique en 3D
def traceHarmonique3D (n, l, m):
    # définit l'espace de tracé
    phi = np.linspace (0, np.pi, 200)
    theta = np.linspace (0, 2*np.pi, 200)
    phi, theta = np.meshgrid (phi, theta)

    # calcule les harmoniques et les coordonnées associées
    psi = abs (harmoniqueSpherique (theta, phi, l, m))
    x = np.sin (phi) * np.cos (theta) * psi
    y = np.sin (phi) * np.sin (theta) * psi
    z = np.cos (phi) * psi

    # définit la palette de couleur
    mini = psi.min ()
    maxi = psi.max ()
    if mini == maxi:
      mini = -0.1
      maxi = 0.1
    fcolors = (psi - mini) / (maxi - mini)
    # trace les harmoniques
    fig = plt.figure (figsize = (20, 16))
    ax = fig.add_subplot (111, projection='3d')
    ax.plot_surface (x, y, z, facecolors=cm.seismic(fcolors), alpha=0.3)
    # trace la projection sur les axes
    cset = ax.contour (x, y, z, 20, zdir='x', offset = -1, cmap='autumn')
    cset = ax.contour (x, y, z, 20, zdir='y', offset =  1, cmap='winter' )
    cset = ax.contour (x, y, z, 20, zdir='z', offset = -1, cmap='summer')
    # légende du graphe
    plt.title (f"$|Y_l^m|, \; l,m={l,m}$", fontsize=20)
    plt.xlabel ('X', fontsize=20)
    plt.ylabel ('Y', fontsize=20)
    # pour avoir un graphe carré
    ax.set_xlim (-1, 1)
    ax.set_ylim (-1, 1)
    ax.set_zlim (-1, 1)


# trace les fonctions d'ondes pour n = 0, ..., 5
nMin = 0
nMax = 5
for n in range (nMin, nMax):
    for l in range (n):
        for m in np.linspace (-l, l, 2*l + 1, dtype=(int)):
            traceDensitePresence (n, l, m)
            plt.show ()
            traceHarmonique3D (n, l, m)
            plt.show ()
