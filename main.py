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

def algo_naive(points):
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

def in_band(points_list, xmin, xmax):
    "Takes a list of points and returns a list of points in that band"
    new_list = []
    for point in points_list:
        abscissa = point.coordinates[0]
        if xmin < abscissa < xmax:      # Condition if the point is in the band
            new_list.append(point)
    return new_list


def extraction(table, sep):
    "Takes a table sorted by increasing y and returns two tables"
    tab1y = []
    tab2y = []
    for point in table:
        if point.coordinates[0] <= sep:     # If x < sep ...
            tab1y.append(point)             # we put in tab2
        else:
            tab2y.append(point)
    return tab1y, tab2y

def min_center(middle_band_points):
    "Do the divide and conquer combination step"
    min_total = math.inf        # Initializing properly
    couple_min = None
    if len(middle_band_points)<2:      # Recursion stop condition
        return math.inf, None           # No couple of points so can't have the minimum

    list_min_band = [None for _ in range(len(middle_band_points))]
     # We look at the points located in a band of width 7 cells (1 cell per point)
    for j in range(0,len(middle_band_points)):
        for i in range(1,8):
            if i+j >= len(middle_band_points):     # We do not leave the width of the table
                pass
            else:
                dist = Point.distance_to(middle_band_points[j], middle_band_points[i+j])
                if dist < min_total:
                    min_total = dist
                    couple_min = (middle_band_points[j], middle_band_points[i+j])
        list_min_band[j] = min_total      # The minimum of the j column
    point1 = str(couple_min[0].coordinates[0]) + ", " + str(couple_min[0].coordinates[1])
    point2 = str(couple_min[1].coordinates[0]) + ", " + str(couple_min[1].coordinates[1])
    couple_return = point1 + "; " + point2
    return min_total, couple_return


def recursive_part(tab_x, tab_y):
    "recursive part of divide and conquer"
    if len(tab_x)<=3:       # From 3 points we do the naive algo
        return algo_naive(tab_x)

    # We divide the table of x into 2
    table1_x = tab_x[:int(len(tab_x)/2)+1]
    table2_x = tab_x[int(len(tab_x)/2):]
    milieu = ((table1_x[-1]+table2_x[0])/2).coordinates[0]      # separator of the two tables
    tab1y, tab2y = extraction(tab_y, milieu)    # We retrieve the y-tabs accordingly

    dist_left, couple_left = recursive_part(table1_x,tab1y)
    dist_right, couple_right = recursive_part(table2_x, tab2y)

    # dist_side = min(dist_left, dist_right)
    if dist_left > dist_right:
        dist_side, couple_side = dist_right, couple_right
    else:
        dist_side, couple_side = dist_left, couple_left
    # In band gives the points in the band, we calculate
    min_band, couple_band = min_center(in_band(tab_y, milieu - dist_side, milieu + dist_side))

    if min_band > dist_side:
        return dist_side, couple_side
    return min_band, couple_band

def divide_and_conquer(points):
    "divide and conquer algorithm"
    tab_x = sorted(points, key = lambda x: x.coordinates[0]) #List of points by increasing x
    tab_y = sorted(points, key = lambda x: x.coordinates[1]) # List of points by increasing y
    return recursive_part(tab_x,tab_y)


# Different test functions

def comparatif():
    """
    Compare the times of the naive solution with those of divide and conquer
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        start = time.time()
        mini_divide = divide_and_conquer(points)
        time_divide = time.time() - start

        start = time.time()
        sol_naive, _ = algo_naive(points)
        time_naive = time.time() - start
        if sol_naive == mini_divide:
            #Format: time_divide , time_naïf  //todo
            return str(time_divide) + "," + str(time_naive)
        print("Error: not the right result")
        return False

def main():
    """
    do not modify: load given instances and display solutions
    """
    for instance in argv[1:]: #in argv[1:]
        points = load_instance(instance)
        _, couple = divide_and_conquer(points)
        print(couple)

def comparator(nb_iteration):
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
        dist_div , _ = divide_and_conquer(points)
        dist_naive , _ = algo_naive(points)
        if dist_div == dist_naive:
            print("Ok")
        else:
            print(dist_div, dist_naive)
            print("Error")
            break

def trace_graphe():
    """
    Draw the comparative graph of the execution times of the two algorithms
    """
    list_time_naive = []
    list_time_divide = []
    list_nb_points = []
    with open("fichier_resultat.txt", 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            ligne = ligne.split(",")
            list_time_divide.append(float(ligne[0]))
            list_time_naive.append(float(ligne[1]))
            list_nb_points.append(float(ligne[2]))

    plt.plot(list_nb_points,list_time_naive, label = "naive algo", color = "mediumblue")

    #On fait une modélisation de degré 2 pour l'algo naïf
    coeff = np.polyfit(list_nb_points, list_time_naive, 2)
    modele_carre = [coeff[2] + coeff[1] * val + coeff[0] * val**2 for val in list_nb_points]
    label_str = f"Modeling : y = {coeff[0]}x² + {coeff[1]:.5f}x"
    plt.plot(list_nb_points, modele_carre,'-.', color = "purple", label = label_str)

    plt.plot(list_nb_points, list_time_divide ,label = "divide and conquer", color="orange")
    plt.title("time execution time of the algos according to the number of points")
    plt.legend()
    plt. xlabel("nb de points")
    plt.ylabel("time")
    plt.show()

main()
