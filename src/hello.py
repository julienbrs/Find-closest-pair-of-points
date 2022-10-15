#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
example of use of the geo module
"""
from math import cos, sin, pi
from itertools import islice, cycle

from geo.point import Point
from geo.tycat import tycat
from geo.segment import Segment


def main():
    """
        small example on the use of tycat
    """
    print("launch me in terminology")
    print("tycat can display points and segments")
    print("each argument must be an iterable on points \
and/or segments (or just one point/segment)")
    print("each argument is displayed in a different color")

    # a point
    origine = Point([0.0, 0.0])
    # a vector of points
    cercle = [Point([cos(c*pi/10), sin(c*pi/10)]) for c in range(20)]
    seg = Segment([Point([1.0, 0.0]), Point([0.0, 1.0])])
    tycat(seg)
    # an iterator on segments (created on the fly)
    segments = (
        Segment([p1, p2])
        for p1, p2 in zip(cercle, islice(cycle(cercle), 1, None))
        )
    tycat(origine, cercle, segments)


main()
