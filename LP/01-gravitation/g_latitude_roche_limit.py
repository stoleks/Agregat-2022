from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math


# quelques constantes pour la Terre
R_Terre = 6.371e6
M_Terre = 5.973e24
V_Terre = 4/3 * np.pi * R_Terre**3
jourSideral_Terre = 23*3600 + 56*60
Omega_Terre = (2*np.pi / jourSideral_Terre)

# quelques constantes pour la Lune
R_Lune = 0.273 * R_Terre
M_Lune = 7.347e22
V_Lune = 4/3 * np.pi * R_Lune**3
rho_Lune = M_Lune / V_Lune

# quelques constantes du système solaire
M_Soleil = 1.989e30
distanceTerreLune = 3.84e8
distanceTerreSoleil = 1.496e9

# constante gravitationnelle
G = 6.674e-11


# pour calculer la limite de Roche
def roche_limit (rho_s, rho_P) :
    return (16 * rho_P  / rho_s)**(1/3)
vec_roche = np.vectorize (roche_limit)

# pour afficher des nombre au format scientifique
def fmt_science (number) :
    return "{:.4e}".format (number)

# calcul la latitude en fonction de la colatitude en degré
def latitude (colatitude) :
    return np.pi * (1/2 - colatitude / 180)

# pour calculer g en fonction de la colatitude en degré
def pesanteur (theta) :
    gravite_Terre = G * M_Terre / R_Terre**2
    rotation_Terre = np.sin (latitude (theta))**2 * R_Terre * Omega_Terre**2
    return gravite_Terre - rotation_Terre
vec_pesanteur = np.vectorize (pesanteur)


# pour calculer le champ de marée
def maree (r, d, theta, x, M_P) :
    facteur = G * M_P / d**3
    return facteur * (x - 3 * r * np.cos (theta) / d)
v_maree = np.vectorize (pesanteur)

# pour calculer la norme de x, y, z
def norme (x, y, z) :
    return np.sqrt (x*x + y*y + z*z)
v_norme = np.vectorize (pesanteur)

def angle (x1, y1, z1, x2, y2, z2) :
    norme1 = norme (x1, y1, z1)
    norme2 = norme (x2, y2, z2)
    return (x2 - x1) + (y2 - y1) + (z2 - z1) / (norme1 * norme2)
v_angle = np.vectorize (pesanteur)


# pesanteur à Paris
g = pesanteur (48.51)
theta = np.arange (0.0, 90.0, 2)
g_theta = vec_pesanteur (theta)
print (fmt_science (g))
print (jourSideral_Terre)
print (fmt_science (Omega_Terre))
plt.plot (theta, g_theta)
plt.xlabel ("Colatitude $[degré]$")
plt.ylabel ("g $[m.s^{-2}$")
plt.show ()


# champ de pesanteur
fig = plt.figure ()
ax = fig.gca (projection='3d')
x, y, z = np.meshgrid (
    np.arange(80, 100, 0.8),
    np.arange(80, 100, 0.8),
    np.arange(80, 100, 0.8)
  )
d_x = distanceTerreSoleil
d_y = distanceTerreSoleil
d_z = distanceTerreSoleil
angles = v_angle (x, y, z, d_x, d_y, d_z)
normesT = v_norme (x, y, z)
normesD = v_norme (d_x, d_y, d_z)
u = maree (normesT, normeSD, angles, x, M_Lune)
v = maree (normesT, normeSD, angles, y, M_Lune)
w = maree (normesT, normeSD, angles, z, M_Lune)
ax.quiver (x, y, z, u, v, w, length = 1.0, color = 'black')
plt.show ()


# limite de Roche pour la lune
limit_lune = R_Terre * roche_limit (rho_Lune, rho_Terre)
print (fmt_science (limit_lune))

# limite de Roche en fonction de la densité
rho = np.arange (0.1, 1e4)
d = vec_roche (rho, rho_Terre)
plt.plot (rho, d)
plt.xlabel ("Densité $[kg.m^{-3}]$")
plt.ylabel ("Limite de Roche $R / R_T$")
plt.show ()
