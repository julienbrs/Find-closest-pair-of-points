#!/usr/bin/env python3
""" Find the two closest points in a point cloud and calculate this distance"""
import time
import subprocess
from sys import argv
from itertools import combinations
import math
import matplotlib.pyplot as plt
import numpy as np
from geo.point import Point

def load_instance(filename):
    """
    loads .mnt file.
    returns list of points.
    """
    with open(filename, "r", encoding="utf-8") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]
    return points


#### Different possible algorithms:


#Naive algorithm

def algo_naif(points):
    "Takes a point cloud and returns the closest pair of points and the distance"
    couples = combinations(points, 2)
    dist_min = math.inf  # initializing properly
    couple_min = None
    for couple in couples:      # testing all combinations of couples
        dist = Point.distance_to(couple[0], couple[1])
        if dist < dist_min:
            dist_min = dist
            couple_min = couple
    # formatting of the string to be sent back
    point1 = str(couple_min[1].coordinates[0]) + ", " + str(couple_min[1].coordinates[1])
    point2 = str(couple_min[0].coordinates[0]) + ", " + str(couple_min[0].coordinates[1])
    couple_return = point1 + "; " + point2
    return dist_min, couple_return


# Divide and conquer algorithm

def dans_bande(liste_points, xmin, xmax):
    "Prend une liste de points et renvoie une liste des points dans cette bande"
    nouvelle_liste = []
    for point in liste_points:
        abscisse = point.coordinates[0]
        if xmin < abscisse < xmax:      # Condition if the point is in the band
            nouvelle_liste.append(point)
    return nouvelle_liste


def extraction(tableau, sep):
    "Prend un tableau triés par y croissants et renvoie deux tableaux"
    tab1y = []
    tab2y = []
    for point in tableau:
        if point.coordinates[0] <= sep:     # If x < sep ...
            tab1y.append(point)             # we put in tab2
        else:
            tab2y.append(point)
    return tab1y, tab2y

def min_centre(points_bande_milieu):
    "Fais l'étape de combinaison du diviser pour régner"
    min_total = math.inf        # Initializing properly
    couple_min = None
    if len(points_bande_milieu)<2:      # Recursion stop condition
        return math.inf, None           # No couple of points so can't have the minimum

    liste_min_bande = [None for _ in range(len(points_bande_milieu))]
     # We look at the points located in a band of width 7 cells (1 cell per point)
    for j in range(0,len(points_bande_milieu)):
        for i in range(1,8):
            if i+j >= len(points_bande_milieu):     # We do not leave the width of the table
                pass
            else:
                dist = Point.distance_to(points_bande_milieu[j], points_bande_milieu[i+j])
                if dist < min_total:
                    min_total = dist
                    couple_min = (points_bande_milieu[j], points_bande_milieu[i+j])
        liste_min_bande[j] = min_total      # The minimum of the j column
    point1 = str(couple_min[0].coordinates[0]) + ", " + str(couple_min[0].coordinates[1])
    point2 = str(couple_min[1].coordinates[0]) + ", " + str(couple_min[1].coordinates[1])
    couple_return = point1 + "; " + point2
    return min_total, couple_return


def partie_recursive(tab_x, tab_y):
    "partie récursive du diviser pour régner"
    if len(tab_x)<=3:       # From 3 points we do the naive algo
        return algo_naif(tab_x)

    # We divide the table of x into 2
    tableau1_x = tab_x[:int(len(tab_x)/2)+1]
    tableau2_x = tab_x[int(len(tab_x)/2):]
    milieu = ((tableau1_x[-1]+tableau2_x[0])/2).coordinates[0]      # separator of the two tables
    tab1y, tab2y = extraction(tab_y, milieu)    # We retrieve the y-tabs accordingly

    dist_gauche, couple_gauche = partie_recursive(tableau1_x,tab1y)
    dist_droite, couple_droite = partie_recursive(tableau2_x, tab2y)

    # dist_coté = min(dist_gauche, dist_droite)  //todo
    if dist_gauche > dist_droite:
        dist_coté, couple_coté = dist_droite, couple_droite
    else:
        dist_coté, couple_coté = dist_gauche, couple_gauche
    # In band gives the points in the band, we calculate
    min_bande, couple_bande = min_centre(dans_bande(tab_y, milieu - dist_coté, milieu + dist_coté))

    if min_bande > dist_coté:
        return dist_coté, couple_coté
    return min_bande, couple_bande

def diviser_pr_regner(points):
    "divide and conquer algorithm"
    tab_x = sorted(points, key = lambda x: x.coordinates[0]) #List of points by increasing x
    tab_y = sorted(points, key = lambda x: x.coordinates[1]) # List of points by increasing y
    return partie_recursive(tab_x,tab_y)


# Different test functions

def comparatif():
    """
    Compare the times of the naive solution with those of divide and conquer
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        debut = time.time()
        mini_diviser = diviser_pr_regner(points)
        temps_diviser = time.time() - debut

        debut = time.time()
        sol_naif, _ = algo_naif(points)
        temps_naif = time.time() - debut
        if sol_naif == mini_diviser:
            #Format: time_divide , time_naïf  //todo
            return str(temps_diviser) + "," + str(temps_naif)
        print("Error: not the right result")
        return False

def main():
    """
    do not modify: load given instances and display solutions
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        _, couple = diviser_pr_regner(points)
        print(couple)

def comparateur(nb_iteration):
    """
    Generate point clouds in a text file, and check that the divide and conquer
    gives the right solution.
    """
    nb_points = 1000
    pas = 500
    for _ in range(nb_iteration):
        nb_points += pas
        subprocess.call("./generation_pts.py " + str(nb_points) + " > 1ex.pts", shell=True)
        instance = "1ex.pts"
        points = load_instance(instance)
        dist_div , _ = diviser_pr_regner(points)
        dist_naif , _ = algo_naif(points)
        if dist_div == dist_naif:
            print("Ok")
        else:
            print(dist_div, dist_naif)
            print("Error")
            break

def trace_graphe():
    """
    Draw the comparative graph of the execution times of the two algorithms
    """
    liste_temps_naif = []
    liste_temps_diviser = []
    liste_nb_points = []
    with open("fichier_resultat.txt", 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            ligne = ligne.split(",")
            liste_temps_diviser.append(float(ligne[0]))
            liste_temps_naif.append(float(ligne[1]))
            liste_nb_points.append(float(ligne[2]))

    plt.plot(liste_nb_points,liste_temps_naif, label = "algo naïf", color = "mediumblue")

    #On fait une modélisation de degré 2 pour l'algo naïf
    coeff = np.polyfit(liste_nb_points, liste_temps_naif, 2)
    modele_carre = [coeff[2] + coeff[1] * val + coeff[0] * val**2 for val in liste_nb_points]
    label_str = f"Modélisation : y = {coeff[0]}x² + {coeff[1]:.5f}x"
    plt.plot(liste_nb_points, modele_carre,'-.', color = "purple", label = label_str)

    plt.plot(liste_nb_points, liste_temps_diviser ,label = "diviser pour régner", color="orange")
    plt.title("Temps d'exécution des algos en fonction du nombre de points")
    plt.legend()
    plt. xlabel("nb de points")
    plt.ylabel("temps")
    plt.show()

main()
