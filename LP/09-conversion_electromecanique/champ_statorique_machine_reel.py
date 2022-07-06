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
taille = (1/3, 0.05)
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

# calcul la position d'une bobine décalée
def position (n, deltaTheta, N, decalage):
    theta = angleBobine (n, deltaTheta, N) + enRadian (decalage)
    return (np.cos (theta), np.sin (theta))

"""
Fonctions de tracé générales
"""
# trace un cercle
def traceCercle (figure, pos, rayon, couleur='white', rempli=True, epaisseur=.0):
  cercle = patches.Circle (pos, radius=rayon, color=couleur, fill=rempli, linewidth=epaisseur)
  figure.add_patch (cercle)

# trace une fleche
def traceFleche (figure, base, tete, largeur=1.0, couleur='black'):
    taille = 0.1 * largeur
    figure.arrow (base[0], base[1], tete[0], tete[1], shape='full', lw=largeur, head_width=taille, color=couleur)

# affiche du texte
def traceTexte (figure, pos, texte, couleur='black', vert="bottom", horiz="right"):
    figure.text (pos[0], pos[1], texte, color=couleur, va=vert, ha=horiz)

# initialise les axes d'une figure
def initialiseAxes (figure, x, y):
    figure.set_xlim (x[0], x[1])
    figure.set_ylim (y[0], y[1])
    figure.set_frame_on (False)
    figure.xaxis.set_visible (False)
    figure.yaxis.set_visible (False)


"""
Fonctions pour tracer le moteur
"""
# Pour tracer une encoche à bobine
# r      : rayon rotor + entrefer
# a      : taille encoche
def traceEncoche (figure, r, a, pos):
    # calcule la position de l'encoche et la trace
    rc = r + a/2
    encochePos = (rc*pos[0], rc*pos[1])
    traceCercle (figure, encochePos, 1.1*a)

# Pour tracer le fil d'une bobine entrant ou sortant
def traceBobine (figure, r, a, pos, couleur, sortant):
    # dessine le fil
    rc = r + a/2
    filPos = (rc*pos[0], rc*pos[1])
    traceCercle (figure, filPos, a, 'black', False, .75)
    # dessine son sens
    if sortant :
      traceCercle (figure, filPos, a/2, couleur)
    else :
      lMin = r - a/4
      l = lMin + 3*a/4
      lMax = lMin + 7*a/4
      # trait vertical
      croixV = ([lMin*pos[0], lMax*pos[0]], [lMin*pos[1], lMax*pos[1]])
      figure.plot (croixV[0], croixV[1], color=couleur, linewidth=1.0)
      # trait horizontal
      croixH = ([l*pos[0] - 0.9*a*pos[1], l*pos[0] + 0.9*a*pos[1]],
          [l*pos[1] + 0.9*a*pos[0], l*pos[1] - 0.9*a*pos[0]])
      figure.plot (croixH[0], croixH[1], color=couleur, linewidth=1.0)

# pour tracer le stator et le rotor
def traceMachine (fig, r, couleur):
    # trace le stator, l'entrefer et le rotor
    traceCercle (fig, (0, 0), r, couleur, True)
    traceCercle (fig, (0, 0), 3*r/4)
    traceCercle (fig, (0, 0), 2*r/3, couleur)

# trace un bobinage
def traceBobinage (fig, r, a, pos, couleur, sortant=True):
    traceEncoche (fig, r, a, pos)
    traceBobine (fig, r, 0.9*a, pos, couleur, sortant)

# trace le moteur synchrone
def traceMoteurSynchrone (N, deltaTheta, triphasee, fig):
    fig.clear ()
    # Zone de tracé
    initialiseAxes (fig, (-3, 3), (-3, 3))
    fig.set_aspect ('equal')
    traceTexte (fig, (-.7, -3), r'$\alpha_{max}=$' + f'{0 : 3.1f}' + '°', vert="top", horiz="left")

    # trace la machine
    traceMachine (fig, 2.9, 'grey')
    r = 2.3
    decalage = 0.1
    a = decalage - 0.001*N
    couleur='dodgerblue'
    # premier jeu de bobine
    for i in range (0, N):
        traceBobinage (fig, r, a, position (i, deltaTheta, N,  90), couleur)
        traceBobinage (fig, r, a, position (i, deltaTheta, N, 270), couleur, False)
    if triphasee:
        # second jeu
        couleur='crimson'
        for i in range (0, N):
            traceBobinage (fig, r + 2.1*decalage, a, position (i, deltaTheta, N, 210), couleur)
            traceBobinage (fig, r + 2.1*decalage, a, position (i, deltaTheta, N,  30), couleur, False)
        # troisieme jeu
        couleur='limegreen'
        for i in range (0, N):
            traceBobinage (fig, r + 4.2*decalage, a, position (i, deltaTheta, N, 330), couleur)
            traceBobinage (fig, r + 4.2*decalage, a, position (i, deltaTheta, N, 150), couleur, False)


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
        traceFleche (figure, (ri*cosi, ri*sini), (l*cost*cosi, l*cost*sini))
    # trace le champ total et affiche son angle
    base = [-r/2 * np.cos (deuxPi * t), 0]
    tete = [r * np.cos (deuxPi * t), 0]
    texteAngle = f'{(1 - np.sign (np.cos (deuxPi*t))) * 90 : 3.1f}'
    if triphasee:
        base[1] = -r/2 * np.sin (deuxPi * t)
        tete[1] = r * np.sin (deuxPi * t)
        texteAngle = f'{360 * t : 3.1f}'
    traceFleche (figure, base, tete, 1.3, 'midnightblue')
    figure.texts[0].set_text (r'$\alpha_{max}=$' + texteAngle + '°')

# initialise le diagramme du champ
def initialiseDiagramme (figure):
    x = np.linspace (xmin, xmax, 150)
    figure.plot (x, 5*np.cos (x), 'darkorange')
    figure.plot (x, champTotal (x, 0, 1, 0, False), 'midnightblue')

# trace les axes du diagrammes B(theta)
def traceAxes (figure):
    # zone de tracé du diagramme
    m = 1 # marge
    initialiseAxes (figure, (xmin - m, xmax + m), (ymin - m, ymax + m))
    # paramètres des axes
    taille = 0.4
    # axe theta
    traceFleche (figure, (xmin - taille, 0), (xmax - xmin + 2*taille, 0))
    traceTexte (figure, (xmax + taille, taille/2), r'$\alpha$')
    # axe B
    traceFleche (figure, (0, ymin - taille), (0, ymax - ymin + 3*taille))
    traceTexte (figure, (taille/2, ymax + 2.4*taille), '$B_s$')


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
