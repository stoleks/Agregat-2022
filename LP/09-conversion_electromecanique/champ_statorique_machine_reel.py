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
grille = fenetre.add_gridspec (ncols=8, nrows=6)
diagramme = fenetre.add_subplot (grille [0:5,0:5])
synchrone = fenetre.add_subplot (grille [1:4,5:8])
plt.rcParams.update({'font.size': 18})

# definition des bouttons réglables
couleurAxe = 'white'
# choix du nombre de bobines
bobines = plt.axes ([0.62, .95, .33, 0.03], facecolor=couleurAxe)
choixNombreBobine = Slider (bobines, 'N  ', 1, 2*7 + 1, valinit=1, valstep=2)
# évolution temporelle
temps = plt.axes ([0.62, 0.9, .33, 0.03], facecolor=couleurAxe)
choixTemps = Slider (temps, '$t/T$  ', 0, 1, valinit=0, valstep=0.01)
# choix mono ou triphasée
monoPhasee = plt.axes ([0.6, 0.18, 0.25, 0.05])
choixPhase = Button (monoPhasee, 'Triphasée')
# choix de tracer le champ dans l'entrefer
champ = plt.axes ([0.6, 0.12, 0.25, 0.05])
tracerChamp = Button (champ, 'Cacher champ entrefer')
# choix de lancer l'animation
animation = plt.axes ([0.86, 0.12, 0.11, 0.11])
lancerAnimation = Button (animation, 'Lancer\n animation')

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
# theta0 : angle initial
# N      : nombre de bobines
def angleBobine (n, theta0, N):
    return (n - (N - 1)/2) * theta0


"""
Fonctions pour tracer le moteur
"""
# Pour tracer une encoche à bobine
# r      : rayon rotor + entrefer
# a      : taille encoche
# theta  : angle de l'encoche (radian)
# figure : figure où tracer l'encoche
def traceEncoche (r, a, theta, figure):
    # calcul position de l'encoche
    cos = np.cos (theta)
    sin = np.sin (theta)
    rc = r + a/2
    encochePos = (rc*cos, rc*sin)
    # dessine un cercle blanc
    encoche = patches.Circle (encochePos, radius=1.1*a, color='white', fill=True)
    figure.add_patch (encoche)

# Pour tracer le fil d'une bobine entrant ou sortant
def traceBobine (r, a, theta, sortant, couleur, figure):
    # dessine le fil
    cos = np.cos (theta)
    sin = np.sin (theta)
    rc = r + a/2
    filPos = (rc*cos, rc*sin)
    fil = patches.Circle (filPos, radius=a, color=couleur, linewidth=0.5, fill=False)
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
      croixV = [[lMin*cos, lMax*cos], [lMin*sin, lMax*sin]]
      figure.plot (croixV[0], croixV[1], color=couleur, linewidth=0.5)
      # trait horizontal
      croixH = [[l*cos - 0.9*a*sin, l*cos + 0.9*a*sin], [l*sin + 0.9*a*cos, l*sin - 0.9*a*cos]]
      figure.plot (croixH[0], croixH[1], color=couleur, linewidth=0.5)

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
def traceBobinage (r, a, i, theta0, N, decalage, sortant, couleur, figure):
    theta = angleBobine (i, theta0, N) + enRadian (decalage)
    traceEncoche (r, a, theta, figure)
    traceBobine (r, a, theta, sortant, couleur, figure)

# trace le moteur synchrone
def traceMoteurSynchrone (N, theta0, triphasee, figure):
    figure.clear ()
    # Zone de tracé de la visualisation du train et du tunnel
    figure.set_xlim (-3, 3)
    figure.set_ylim (-3, 3)
    figure.set_frame_on (False)
    figure.xaxis.set_visible (False)
    figure.yaxis.set_visible (False)
    figure.set_aspect ('equal')
    figure.text (-.7, -3, r'$\theta_{max}=$'+f'{0 : 3.1f}'+'°', color='black', va="top", ha="left")

    # trace la machine
    traceMachine (2.9, 'grey', figure)
    r = 2.3
    decalage = 0.1
    a = decalage - 0.001*N
    couleur='k'
    # premier jeu de bobine
    for i in range (0, N):
        traceBobinage (r, a, i, theta0, N,  90, True, couleur, figure)
        traceBobinage (r, a, i, theta0, N, 270, False, couleur, figure)
    # second et troisieme jeu de bobine
    if triphasee:
        # second jeu
        couleur='r'
        for i in range (0, N):
            traceBobinage (r + 2.1*decalage, a, i, theta0, N, 210, True, couleur, figure)
            traceBobinage (r + 2.1*decalage, a, i, theta0, N,  30, False, couleur, figure)
        # troisieme jeu
        couleur='g'
        for i in range (0, N):
            traceBobinage (r + 4.2*decalage, a, i, theta0, N, 330, True, couleur, figure)
            traceBobinage (r + 4.2*decalage, a, i, theta0, N, 150, False, couleur, figure)


"""
Fonction pour tracer le champ
"""
# trace le champ dans l'entrefer
# r : taille de la machine
# l : longueur des vecteurs
def traceVecteurChamp (t, r, l, triphasee, figure):
    # trace le champ des bobine
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
            shape='full', lw=.75, length_includes_head=False, head_width=.05, color='black')
    # trace le champ total et affiche son angle
    baseX = -r/2 * np.cos (deuxPi * t)
    teteX = r * np.cos (deuxPi * t)
    baseY = 0
    teteY = 0
    texteAngle = f'{(1 - np.sign (np.cos (deuxPi*t))) * 90 : 3.1f}'
    if triphasee:
        baseY = -r/2 * np.sin (deuxPi * t)
        teteY = r * np.sin (deuxPi * t)
        texteAngle = f'{360 * t : 3.1f}'
    figure.arrow (baseX, baseY, teteX, teteY,
        shape='full', lw=1.3, length_includes_head=True, head_width=.3, color='blue')
    figure.texts[0].set_text (r'$\theta_{max}=$' + texteAngle + '°')

# trace le diagramme du champ
def traceValeurChamp (N, theta0, t, figure):
    x = np.linspace (xmin, xmax, 300)
    figure.plot (x, 5*np.cos(x), 'r-')
    figure.plot (x, champTotal (x, theta0, t, N), 'b-')

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
    figure.text (xmax + taille, taille/2, r'$\theta$',
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
    if d < -3.5 or d > -2.5 and d < -1.5 or d > -0.5 and d < 0.5  or d > 1.5 and d < 2.5  or d > 3.5:
        return True
    return False


# calcul du champ d'une bobine
def champ (theta, theta0, t):
    deuxPi = 2*np.pi
    x = theta - theta0
    for i in range (0, 300):
        if positif (x[i] / np.pi):
            x[i] = 5*np.cos (deuxPi*t)
        else:
            x[i] = -5*np.cos (deuxPi*t)
    return x

# calcul du champ total
def champTotal (theta, theta0, t, N):
    val = 0
    for i in range (0, N):
        angle = angleBobine (i, theta0, N)
        val = val + champ (theta, angle, t) / N
    return val


"""
Fonctions de mise à jour
"""
# mise à jour des paramètres
def miseAJour (val):
    N = choixNombreBobine.val
    theta0 = enRadian (180) / (N + 1)
    if N == 1:
        theta0 = 0
    triphasee = choixPhase.label.get_text () == 'Monophasée'
    traceMoteurSynchrone (N, theta0, triphasee, synchrone)
    if tracerChamp.label.get_text () == 'Cacher champ entrefer':
        t = choixTemps.val
        traceVecteurChamp (t, 2, 0.4, triphasee, synchrone)
    x = np.linspace (xmin, xmax, 300)
    if not triphasee:
        diagramme.lines[1].set_data (x, champTotal (x, theta0, 0, N))

# anime
def animer (i):
    deltaT = i / 24
    t = deltaT - np.floor (deltaT)
    if lancerAnimation.label.get_text() == 'Arrêter\n animation':
        choixTemps.set_val (t)
        miseAJour (0)


"""
Fonction d'interface
"""
def choixMonoOuTriphasee (val):
    if choixPhase.label.get_text() == 'Triphasée':
        diagramme.lines[1].remove ()
        choixPhase.label.set_text ('Monophasée')
    else:
        diagramme.plot ([0,0], [0,0], 'b-')
        choixPhase.label.set_text ('Triphasée')
    choixNombreBobine.set_val (1)
    miseAJour (0)

def choixTracerChamp (val):
    if tracerChamp.label.get_text () == 'Montrer champ entrefer':
        tracerChamp.label.set_text ('Cacher champ entrefer')
    else:
        tracerChamp.label.set_text ('Montrer champ entrefer')
    choixNombreBobine.set_val (1)
    miseAJour (0)

def choixLancerAnimation (val):
    if lancerAnimation.label.get_text() == 'Lancer\n animation':
        lancerAnimation.label.set_text ('Arrêter\n animation')
    else:
        lancerAnimation.label.set_text ('Lancer\n animation')
    choixNombreBobine.set_val (1)
    miseAJour (0)


"""
Partie principale
"""
# trace les axes et défini le nombre de bobines
traceAxes (diagramme)
N = choixNombreBobine.val
t = choixTemps.val
theta0 = 2.63 / (N + 1)
if N == 1:
    theta0=0
triphasee = choixPhase.label.get_text () == 'Monophasée'
traceMoteurSynchrone (N, theta0, triphasee, synchrone)
traceVecteurChamp (t, 2, 0.4, triphasee, synchrone)
traceValeurChamp (N, theta0, t, diagramme)

# mise à jour interactive
choixNombreBobine.on_changed (miseAJour)
choixTemps.on_changed (miseAJour)
choixPhase.on_clicked (choixMonoOuTriphasee)
tracerChamp.on_clicked (choixTracerChamp)
lancerAnimation.on_clicked (choixLancerAnimation)

# lance l'animation
ani = anim.FuncAnimation (fenetre, animer, 100)

plt.show()
