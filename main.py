#!/usr/bin/env python3

from timeit import timeit
from sys import argv
from geo.point import Point
from itertools import combinations
import math
import geo.tycat
import geo.segment as segment

#### Différents algorithmes possibles:

def algo_naif(points):
    couples = combinations(points, 2)
    dist_min = math.inf  #on initialise proprement
    for couple in couples:
        dist = Point.distance_to(couple[0], couple[1])
        if dist < dist_min:
            dist_min = dist
    return dist

def display_naif(points):
    couples = combinations(points, 2)
    dist_min = math.inf  #on initialise proprement
    geo.tycat.tycat(points)
    for couple in couples:
        dist = Point.distance_to(couple[0], couple[1])
        if dist < dist_min:
            dist_min = dist
            nouv_seg = segment.Segment([couple[0], couple[1]])
            geo.tycat.tycat(*[points, nouv_seg])
    return dist



def load_instance(filename):
    """
    loads .mnt file. 
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]

    return points


def print_solution(points):
    """
    calcul et affichage de la solution (a faire)
    """
    display_naif(points)



def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)

main()

