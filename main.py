#!/usr/bin/env python3
""" Trouve les deux points les plus proches parmi un nuage de points et calcule cette distance"""
#from asyncio import subprocess
#from re import A
#from timeit import timeit
import time
from sys import argv
import subprocess
import math
from itertools import combinations
from geo.point import Point
#import geo.tycat
#from geo import segment
#### Différents algorithmes possibles:

def algo_naif(points):
    "Prend un nuage de points et renvoie le couple de points le plus proche ainsi que la distance"
    couples = combinations(points, 2)
    dist_min = math.inf  #on initialise proprement
    couple_min = None
    for couple in couples:
        dist = Point.distance_to(couple[0], couple[1])
        if dist < dist_min:
            dist_min = dist
            couple_min = couple
    point1 = str(couple_min[0].coordinates[0]) + ", " + str(couple_min[0].coordinates[1])
    point2 = str(couple_min[1].coordinates[0]) + ", " + str(couple_min[1].coordinates[1])
    couple_return = point1 + "; " + point2
    return dist_min, couple_return


def load_instance(filename):
    """
    loads .mnt file.
    returns list of points.
    """
    with open(filename, "r", encoding="utf-8") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points


def dans_bande(liste_points, xmin, xmax):
    "Prend une liste de points et renvoie une liste des points dans cette bande"
    nouvelle_liste = []
    for point in liste_points:
        abscisse = point.coordinates[0]
        if xmin < abscisse < xmax:
            nouvelle_liste.append(point)
    return nouvelle_liste



def extraction(tableau, sep):
    "Prend un tableau triés par y croissants et renvoie deux tableaux"
    tab1y = []
    tab2y = []
    for point in tableau:
        if point.coordinates[0] <= sep:
            tab1y.append(point)
        else:
            tab2y.append(point)
    return tab1y, tab2y

def plus_proches_centre(points_bande_milieu):
    "Fais l'étape de combinaison du diviser pour régner"
    min_total = math.inf
    couple_min = None
    if len(points_bande_milieu)<2:
        return math.inf, None
    liste_min_bande = [None for _ in range(len(points_bande_milieu))]
    for j in range(0,len(points_bande_milieu)):  #tous
        for i in range(1,8):
            if i+j >= len(points_bande_milieu):
                pass
            else:
                dist = Point.distance_to(points_bande_milieu[j], points_bande_milieu[i+j])
                if dist < min_total:
                    min_total = dist
                    couple_min = (points_bande_milieu[j], points_bande_milieu[i+j])
        liste_min_bande[j] = min_total
    point1 = str(couple_min[0].coordinates[0]) + ", " + str(couple_min[0].coordinates[1])
    point2 = str(couple_min[1].coordinates[0]) + ", " + str(couple_min[1].coordinates[1])
    couple_return = point1 + "; " + point2
    return min_total, couple_return

def partie_recursive(tableau_x, tableau_y):
    "partie récursive du main"
    if len(tableau_x)<=3:
        minimum_naif, couple_naif = algo_naif(tableau_x)
        return minimum_naif, couple_naif
    ntab = len(tableau_x)
    tableau1_x = tableau_x[:int(ntab/2)]
    tableau2_x = tableau_x[int(ntab/2):]
    milieu = ((tableau1_x[-1]+tableau2_x[0])/2).coordinates[0]
    tab1y, tab2y = extraction(tableau_y, milieu)
    deltag, ming = partie_recursive(tableau1_x,tab1y)
    deltad, mind = partie_recursive(tableau2_x, tab2y)
    if deltag > deltad:
        delta_final, couple_delta = deltad, mind
    else:
        delta_final, couple_delta = deltag, ming
    tableau_bande = dans_bande(tableau_y, milieu-delta_final, milieu+delta_final)
    min_bande, couple_bande = plus_proches_centre(tableau_bande)
    if min_bande > delta_final:
        return delta_final, couple_delta
    return min_bande, couple_bande


def plusproches(points):
    "algorithme diviser pour régner"
    tableau_x = sorted(points, key = lambda x: x.coordinates[0]) #Liste de pts par x croissants
    tableau_y = sorted(points, key = lambda x: x.coordinates[1]) #Liste de pts par y croissants
    return partie_recursive(tableau_x,tableau_y)

def main_comparatif():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        debut = time.time()
        mini_diviser = plusproches(points)
        temps_diviser = time.time() - debut
        debut = time.time()
        sol_naif, _ = algo_naif(points)
        temps_naif = time.time() - debut
        if sol_naif == mini_diviser:
            return str(temps_diviser) + "," + str(temps_naif)
        return False

def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        debut = time.time()
        distance_mini, couple = plusproches(points)
        temps_diviser = time.time() - debut
        print(couple)

def comparateur(nb_iteration):
    "Compare plein de test ainsi que les temps des deux algos"
    nb_points = 100
    pas = 200
    for _ in range(nb_iteration):
        nb_points += pas
        subprocess.call("./generation_pts.py " + str(nb_points) + " > 1ex.pts", shell=True)
        resultat = str(main()) + "," + str(nb_points)
        print(resultat)

def analyse_poussee():
    """
    Analyse pousée des perfs
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        debut = time.time()
        mini_diviser = plusproches(points)
        temps_diviser = time.time() - debut
        print(mini_diviser, "et le temps est: ", temps_diviser)

#comparateur(10)
main()
