# -*- coding: utf-8 -*-
__title__ = "Distance Calc"
__doc__ = """______"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import sys
import math
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import forms, revit

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
rvt_year = int(app.VersionNumber)

# CLASSES

def feet_to_mm(feet):
    inches = feet * 12
    mm = inches * 25.4
    return mm


def calculate_distance(point1, point2):
    distance = abs(point2 - point1)
    return distance


def find_minimum_value(values):
    min_value = float('inf')  # Initialize with a large value

    for value in values:
        if value < min_value:
            min_value = value

    return min_value


# MAIN
# ==================================================


# PICK ELEMENT

with forms.WarningBar(title='Pick an Element:'):
    element = revit.pick_element()

element_type = type(element)

if element_type != Wall:
    forms.alert('You were supposed to pick a Wall.', exitscript=True)

print('*' * 50)

# GET ALL GRIDS

all_grids = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()
#print(all_grids)

# GRID SORTING

v_grids = []
h_grids = []
for element_id in all_grids:
    # Perform operations on each element ID here

    Grid = doc.GetElement(element_id)

    Grid_orientation = Grid.Curve.Direction.Y
    if Grid_orientation == -1:
        grid_o = "V"
        v_grids.append(element_id)
    elif Grid_orientation != -1:
        grid_o = "H"
        h_grids.append(element_id)

# # Print the extracted element IDs
# for element_id in v_grids:
#     print('{} - Vertical Grid'.format(element_id))
# for element_id in h_grids:
#     print('{} - Horizontal Grid'.format(element_id))

# GET DISTANCE BETWEEN WALL AND GRID

# 1) get wall coordinate and orientation

Wall_x = element.Location.Curve.Origin.X
print('Wall_p1: {}'.format(Wall_x))
Wall_y = element.Location.Curve.Origin.Y
print('Wall_p2: {}'.format(Wall_y))

Wall_orientation = abs(element.Location.Curve.Direction.Y)                          # V==1 & H!=1
print('Wall_orientation: {}'.format(Wall_orientation))

# all_walls = FilteredElementCollector(doc).OfCategory(
#     BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
# for element_id in all_walls:
#     # Perform operations on each element ID here
#     Walla = doc.GetElement(element_id)
#
#     Walla_orientation = abs(Walla.Location.Curve.Direction.Y)
#     print("Element ID: {}, Wall Orientation: {}".format(element_id, Walla_orientation))
#
#
# for element_id in all_grids:
#     # Perform operations on each element ID here
#     Grida = doc.GetElement(element_id)
#
#     Grida_orientation = Grida.Curve.Direction.Y
#     print("Element ID: {}, Grid Orientation: {}".format(element_id, Grida_orientation))

# 2) get coordinates of grids (which are parallel to wall)

distance_grids = []

if Wall_orientation == 1:
    for element_id in v_grids:
        Grid = doc.GetElement(element_id)
        Grid_x = Grid.Curve.Origin.X
        Grid_y = Grid.Curve.Origin.Y

        Wall_mm_value = feet_to_mm(Wall_x)
        Grid_mm_value = feet_to_mm(Grid_x)

        distance = calculate_distance(Wall_mm_value, Grid_mm_value)
        print('Distance(hor): {}'.format(distance))

        distance_grids.append(distance)

    find_minimum_value(distance_grids)

elif Wall_orientation != 1:
    for element_id in h_grids:
        Grid = doc.GetElement(element_id)
        Grid_x = Grid.Curve.Origin.X
        Grid_y = Grid.Curve.Origin.Y

        Wall_mm_value = feet_to_mm(Wall_y)
        Grid_mm_value = feet_to_mm(Grid_y)

        distance = calculate_distance(Wall_mm_value, Grid_mm_value)
        print('Distance(ver): {}'.format(distance))

        distance_grids.append(distance)

    find_minimum_value(distance_grids)

min_distance = find_minimum_value(distance_grids)
print('min_distance: {}'.format(min_distance))

