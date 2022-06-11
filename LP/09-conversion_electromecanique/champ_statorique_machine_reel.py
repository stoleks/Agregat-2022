#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
  Trace le champ statorique d'une machine réelle
"""

#-----------------------------------------------------------------------------
# Tracé du champ dû au stator pour une machine synchrone
#-----------------------------------------------------------------------------

# Bibliothèques utilisées

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as anim
from matplotlib.widgets import Slider, Button


"""
Initialisation
"""
# agancement de la fenêtre
fenetre = plt.figure (constrained_layout=True, figsize=(8,5))
grille = fenetre.add_gridspec (ncols=10, nrows=8)
synchrone = fenetre.add_subplot (grille [1:6,0:5])
diagramme = fenetre.add_subplot (grille [1:6,5:10])
plt.rcParams.update({'font.size': 18})

# definition des bouttons réglables
couleurAxe = 'white'
taille = [1/3, 0.05]
x = 0.08
y = 0.925
espacement = 0.06
# choix du nombre de bobines
bobines = plt.axes ([x, y, taille[0], taille[1]], facecolor=couleurAxe)
choixNombreBobine = Slider (bobines, 'N  ', 1, 2*7 + 1, valinit=1, valstep=2)
# évolution temporelle
temps = plt.axes ([x, y - espacement, taille[0], taille[1]], facecolor=couleurAxe)
choixTemps = Slider (temps, '$t/T$  ', 0, 1, valinit=0, valstep=0.01)
# choix mono ou triphasée
y = 0.15
monoPhasee = plt.axes ([x, y, taille[0], taille[1]])
choixPhase = Button (monoPhasee, 'Triphasée')
# choix de lancer l'animation
animation = plt.axes ([x, y - espacement, taille[0], taille[1]])
lancerAnimation = Button (animation, 'Lancer l\'animation')

# coordonnées du diagramme
xmin = -5
ymin = -5
xmax = 5
ymax = 5
# coordonnées avec les marges
marge = 1
xmin0 = xmin - marge
ymin0 = ymin - marge
xmax0 = xmax + marge
ymax0 = ymax + marge


"""
Fonctions mathématiques
"""
# pour convertir des angles
def enRadian (angle):
    return angle * np.pi / 180

# calcul l'angle de la n-ième bobine
# n      : numéro de la bobine
# N      : nombre de bobines
def angleBobine (n, deltaTheta, N):
    return (n - (N - 1)/2) * deltaTheta


"""
Fonctions pour tracer le moteur
"""
# Pour tracer une encoche à bobine
# r      : rayon rotor + entrefer
# a      : taille encoche
def traceEncoche (r, a, cosTheta, sinTheta, figure):
    # calcul position de l'encoche
    rc = r + a/2
    encochePos = (rc*cosTheta, rc*sinTheta)
    # dessine un cercle blanc
    encoche = patches.Circle (encochePos, radius=1.1*a, color='white', fill=True)
    figure.add_patch (encoche)

# Pour tracer le fil d'une bobine entrant ou sortant
def traceBobine (r, a, cosTheta, sinTheta, sortant, couleur, figure):
    # dessine le fil
    rc = r + a/2
    filPos = (rc*cosTheta, rc*sinTheta)
    fil = patches.Circle (filPos, radius=a, color='black', linewidth=0.5, fill=False)
    figure.add_patch (fil)
    # dessine son sens
    if sortant :
      sens = patches.Circle (filPos, radius=a/3, color=couleur, fill=True)
      figure.add_patch (sens)
    else :
      lMin = r - a/4
      l = lMin + 3*a/4
      lMax = lMin + 7*a/4
      # trait vertical
      croixV = [[lMin*cosTheta, lMax*cosTheta], [lMin*sinTheta, lMax*sinTheta]]
      figure.plot (croixV[0], croixV[1], color=couleur, linewidth=1.0)
      # trait horizontal
      croixH = [[l*cosTheta - 0.9*a*sinTheta, l*cosTheta + 0.9*a*sinTheta],
          [l*sinTheta + 0.9*a*cosTheta, l*sinTheta - 0.9*a*cosTheta]]
      figure.plot (croixH[0], croixH[1], color=couleur, linewidth=1.0)

# pour tracer le stator et le rotor
def traceMachine (r, couleur, figure):
    # trace le stator
    stator = plt.Circle ((0, 0), r, color=couleur, fill=True)
    figure.add_patch (stator)
    # trace l'entrefer
    entrefer = plt.Circle ((0, 0), 3*r/4, color='white', fill=True)
    figure.add_patch (entrefer)
    # trace le rotor
    rotor = plt.Circle ((0, 0), 2*r/3, color=couleur, fill=True)
    figure.add_patch (rotor)

# trace un bobinage
def traceBobinage (r, a, i, deltaTheta, N, decalage, sortant, couleur, figure):
    theta = angleBobine (i, deltaTheta, N) + enRadian (decalage)
    traceEncoche (r, a, np.cos(theta), np.sin(theta), figure)
    traceBobine (r, a, np.cos(theta), np.sin(theta), sortant, couleur, figure)

# trace le moteur synchrone
def traceMoteurSynchrone (N, deltaTheta, triphasee, figure):
    figure.clear ()
    # Zone de tracé de la visualisation du train et du tunnel
    figure.set_xlim (-3, 3)
    figure.set_ylim (-3, 3)
    figure.set_frame_on (False)
    figure.xaxis.set_visible (False)
    figure.yaxis.set_visible (False)
    figure.set_aspect ('equal')
    figure.text (-.7, -3, r'$\alpha_{max}=$'+f'{0 : 3.1f}'+'°', color='black', va="top", ha="left")

    # trace la machine
    traceMachine (2.9, 'grey', figure)
    r = 2.3
    decalage = 0.1
    a = decalage - 0.001*N
    couleur='dodgerblue'
    # premier jeu de bobine
    for i in range (0, N):
        traceBobinage (r, a, i, deltaTheta, N,  90, True, couleur, figure)
        traceBobinage (r, a, i, deltaTheta, N, 270, False, couleur, figure)
    # second et troisieme jeu de bobine
    if triphasee:
        # second jeu
        couleur='crimson'
        for i in range (0, N):
            traceBobinage (r + 2.1*decalage, a, i, deltaTheta, N, 210, True, couleur, figure)
            traceBobinage (r + 2.1*decalage, a, i, deltaTheta, N,  30, False, couleur, figure)
        # troisieme jeu
        couleur='limegreen'
        for i in range (0, N):
            traceBobinage (r + 4.2*decalage, a, i, deltaTheta, N, 330, True, couleur, figure)
            traceBobinage (r + 4.2*decalage, a, i, deltaTheta, N, 150, False, couleur, figure)


"""
Fonction pour tracer le champ
"""
# trace le champ dans l'entrefer
# r : taille de la machine
# l : longueur des vecteurs
def traceVecteurChamp (t, r, l, triphasee, figure):
    # trace le champ dans l'entrefer
    deuxPi = 2*np.pi
    nombreVecteurs = 16
    for i in range (0, nombreVecteurs):
        angle = (i - 8) * deuxPi / nombreVecteurs
        cosi = np.cos (angle)
        sini = np.sin (angle)
        if triphasee:
            cost = np.cos (angle - deuxPi*t)
            sint = np.sin (angle - deuxPi*t)
        else:
            cost = np.cos (angle) * np.cos (deuxPi*t)
            sint = np.sin (angle) * np.cos (deuxPi*t)
        ri = 3*r/4
        figure.arrow (ri*cosi, ri*sini, l*cost*cosi, l*cost*sini,
            shape='full', lw=1.0, length_includes_head=False, head_width=.1, color='black')
    # trace le champ total et affiche son angle
    base = [-r/2 * np.cos (deuxPi * t), 0]
    tete = [r * np.cos (deuxPi * t), 0]
    texteAngle = f'{(1 - np.sign (np.cos (deuxPi*t))) * 90 : 3.1f}'
    if triphasee:
        base[1] = -r/2 * np.sin (deuxPi * t)
        tete[1] = r * np.sin (deuxPi * t)
        texteAngle = f'{360 * t : 3.1f}'
    figure.arrow (base[0], base[1], tete[0], tete[1],
        shape='full', lw=1.3, length_includes_head=True, head_width=.3, color='midnightblue')
    figure.texts[0].set_text (r'$\alpha_{max}=$' + texteAngle + '°')

# initialise le diagramme du champ
def initialiseDiagramme (figure):
    x = np.linspace (xmin, xmax, 150)
    figure.plot (x, 5*np.cos (x), 'darkorange')
    figure.plot (x, champTotal (x, 0, 1, 0, False), 'midnightblue')

# trace les axes du diagrammes B(theta)
def traceAxes (figure):
    # zone de tracé du diagramme
    figure.set_xlim (xmin0, xmax0)
    figure.set_ylim (ymin0, ymax0)
    figure.set_frame_on (False)
    figure.xaxis.set_visible (False)
    figure.yaxis.set_visible (False)
    # paramètres des axes
    taille = 0.4
    # axe theta
    figure.arrow (xmin - taille, 0, xmax - xmin + 2*taille, 0,
        shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
    figure.text (xmax + taille, taille/2, r'$\alpha$',
        color='black', va="bottom", ha="right")
    # axe B
    figure.arrow (0, ymin - taille, 0, ymax - ymin + 3*taille,
        shape='full', lw=.75, length_includes_head=True, head_width=.25, color='black')
    figure.text (taille/2, ymax + 2*taille, "$B_s$",
        color='black', va="bottom", ha="right")


"""
Fonctions de calcul des champs
"""
# détermination du signe du champ
def positif (d):
    if (d < -2):
        d = d + 2
    if (d > 2):
        d = d - 2
    # B > 0 si dans [-π/2, π/2] ou [-2π, -3π/2] U [3π/2, 2π]
    return (d < -1.5 or d > -0.5) and (d < 0.5 or d > 1.5)

# calcul du champ d'une bobine
def champ (theta, angle, t, triphasee):
    Bmax = 5
    x = theta - angle - 2*np.pi*t
    if not triphasee:
        Bmax = 5*np.cos (2*np.pi*t)
        x = x + 2*np.pi*t
    for i in range (0, 150):
        if positif (x[i] / np.pi):
            x[i] = Bmax
        else:
            x[i] = -Bmax
    return x

# calcul du champ total
def champTotal (theta, t, N, deltaTheta, triphasee):
    val = 0
    for i in range (0, N):
        angle = angleBobine (i, deltaTheta, N)
        val = val + champ (theta, angle, t, triphasee) / N
    return val


"""
Fonctions de mise à jour
"""
# mise à jour du système
def miseAJour (val):
    N = choixNombreBobine.val
    deltaTheta = enRadian (180) / N
    triphasee = choixPhase.label.get_text () == 'Monophasée'
    traceMoteurSynchrone (N, deltaTheta, triphasee, synchrone)
    t = choixTemps.val
    traceVecteurChamp (t, 2.7, 0.4, triphasee, synchrone)
    # met à jour les champs
    x = np.linspace (xmin, xmax, 150)
    champSinus = 0
    if triphasee:
        champSinus = 5*np.cos (x - 2*np.pi*t)
    else:
        champSinus = 5*np.cos (x)*np.cos (2*np.pi*t)
    diagramme.lines[0].set_data (x, champSinus)
    diagramme.lines[1].set_data (x, champTotal (x, t, N, deltaTheta, triphasee))

# animation
def animer (i):
    deltaT = i / 30
    t = deltaT - np.floor (deltaT)
    if lancerAnimation.label.get_text() == 'Arrêter l\'animation':
        choixTemps.set_val (t)
        miseAJour (0)


"""
Fonction d'interface
"""
def choixMonoOuTriphasee (val):
    if choixPhase.label.get_text() == 'Triphasée':
        choixPhase.label.set_text ('Monophasée')
    else:
        diagramme.plot ([0,0], [0,0], 'b-')
        choixPhase.label.set_text ('Triphasée')
    miseAJour (0)

def choixLancerAnimation (val):
    if lancerAnimation.label.get_text() == 'Lancer l\'animation':
        lancerAnimation.label.set_text ('Arrêter l\'animation')
    else:
        lancerAnimation.label.set_text ('Lancer l\'animation')
    miseAJour (0)


"""
Partie principale
"""
# trace les axes et défini le nombre de bobines
traceAxes (diagramme)
initialiseDiagramme (diagramme)
miseAJour (0)

# mise à jour interactive
choixTemps.on_changed (miseAJour)
choixNombreBobine.on_changed (miseAJour)
choixPhase.on_clicked (choixMonoOuTriphasee)
lancerAnimation.on_clicked (choixLancerAnimation)

# lance l'animation
ani = anim.FuncAnimation (fenetre, animer, 60, interval = 16)

plt.show()
