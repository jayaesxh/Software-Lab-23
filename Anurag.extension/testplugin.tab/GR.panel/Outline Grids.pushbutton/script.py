# -*- coding: utf-8 -*-
__title__ = "Outline Grids"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk

import sys

import json
import math
import System
import clr
from System.Collections.Generic import List
# clr.AddReference('RevitAPI')
# clr.AddReference('RevitAPIUI')

import sys

from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.__init___parts.DoubleParameterValue import DoubleParameterValue
# from Autodesk.Revit.DB.__init___parts.GlobalParameter import GlobalParameter
# from Autodesk.Revit.DB.__init___parts.ParameterType import ParameterType
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

from Autodesk.Revit.DB import ElementId, GlobalParameter, DoubleParameterValue
from Autodesk.Revit.UI import TaskDialog

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

from Autodesk.Revit.DB import *

# pyRevit

# VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
rvt_year = int(app.VersionNumber)


# MAIN
# ==================================================

def convert_to_flat_dict(input_dict):
    flat_dict = {}
    for key, coordinates_list in input_dict.items():
        for i, coordinates in enumerate(coordinates_list):
            flat_dict['{}_{}'.format(key, i + 1)] = coordinates
    return flat_dict


def orientation(p, q, r):
    """
    Function to find the orientation of triplet (p, q, r).
    The function returns the following values:
    0: Collinear points
    1: Clockwise points
    2: Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise


def atan2(y, x):
    """
    Function to calculate arctangent of y/x without using numpy.
    """
    if x > 0:
        return arctan(y / x)
    elif x < 0 and y >= 0:
        return arctan(y / x) + pi
    elif x < 0 and y < 0:
        return arctan(y / x) - pi
    elif x == 0 and y > 0:
        return pi / 2
    elif x == 0 and y < 0:
        return -pi / 2
    elif x == 0 and y == 0:
        return 0


def arctan(x):
    """
    Function to calculate arctangent without using numpy.
    """
    angle = 0
    x_squared = x * x
    divisor = 1
    term = x / 1

    while term != 0:
        angle += term
        divisor += 2
        term *= -x_squared / divisor
        divisor += 2
        term /= divisor

    return angle


# Constants
pi = 3.141592653589793


def graham_scan(points):
    """
    Function to compute the convex hull of a set of points using the Graham's scan algorithm.
    """
    n = len(points)
    if n < 3:
        return "Convex hull not possible with less than 3 points."

    # Find the point with the lowest y-coordinate (and leftmost if tied)
    pivot = min(points, key=lambda point: (point[1], point[0]))

    # Sort the points based on polar angle from the pivot
    sorted_points = sorted(points, key=lambda point: (atan2(point[1] - pivot[1], point[0] - pivot[0]), point))

    # Initialize the convex hull with the pivot and the first two sorted points
    hull = [pivot, sorted_points[0], sorted_points[1]]

    for i in range(2, n):
        while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != 2:
            hull.pop()
        hull.append(sorted_points[i])

    return hull


# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictA = r'D:\Software Lab Data\Revit_Plug-ins\Anurag.extension\testplugin.tab\Create Dictionary.panel\Create Dictionary.pushbutton\output.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictA, 'r') as file:
    dictA = json.load(file)

print(dictA)
print("Type dictA: ", type(dictA))
print("dictA: {}".format(';'.join(dictA)))

grid_coordinates = []
dictC = {}

for wall_id, grid_id in dictA.items():
    # Get Wall and Grid elements based on their IDs
    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(grid_id)))

    gep0 = grid.Curve.GetEndPoint(0)
    gep1 = grid.Curve.GetEndPoint(1)

    grid_coordinates.append((gep0[0], gep0[1]))
    grid_coordinates.append((gep1[0], gep1[1]))

    print("Coordinates for Wall {}:".format(grid_id))
    print("Endpoint 0: ({}, {})".format(gep0[0], gep0[1]))
    print("Endpoint 1: ({}, {})".format(gep1[0], gep1[1]))
    print('*' * 50)

    # Create dictC entries
    dictC[grid_id] = [(round(gep0[0], 3), round(gep0[1], 3)), (round(gep1[0], 3), round(gep1[1], 3))]

print(grid_coordinates)

print(dictC)
print("Type dictC: ", type(dictC))

rounded_grid_coordinates = [(round(x, 3), round(y, 3)) for x, y in grid_coordinates]

convex_hull = graham_scan(rounded_grid_coordinates)

print("Convex Hull Vertices:", convex_hull)
matching_grid_ids = []
matching_grid_coordinates = []

tolerance = 0.0001

for grid_id, coordinates_list in dictC.items():
    for convex_vertex in convex_hull:
        for coordinates in coordinates_list:
            if all(abs(coord - convex_coord) < tolerance for coord, convex_coord in zip(coordinates, convex_vertex)):
                matching_grid_ids.append(grid_id)

# Remove duplicates by converting to a set and back to a list
matching_grid_ids = list(set(matching_grid_ids))

# print("Grid IDs with Similar Coordinates to Convex Hull:", matching_grid_ids)


print('*' * 50)
matching_grid_ids_str = [str(grid_id) for grid_id in matching_grid_ids]
print("Grid IDs with Similar Coordinates to Convex Hull: {}".format(';'.join(matching_grid_ids_str)))
