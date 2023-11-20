# -*- coding: utf-8 -*-
__title__ = "Get Outermost Grids"
__doc__ = """This script is part of YouTube video
where I explain RevitAPI Parameters and how to work with them.

You can support my channel on:
www.patreon.com/ErikFrits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
import sys
import math
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

# pyRevit
from pyrevit import forms, revit
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================

#VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
rvt_year = int(app.VersionNumber)


def find_minimum_value(values):
    min_value = float('inf')  # Initialize with a large value

    for value in values:
        if value < min_value:
            min_value = value

    return min_value

def find_maximum_value(values):
    max_value = float('-inf')  # Initialize with a small value

    for value in values:
        if value > max_value:
            max_value = value

    return max_value



# MAIN
# ==================================================


# GET ALL WALLS
all_walls = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
# print(all_walls)


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
    if Grid_orientation == 1 or Grid_orientation == -1:
        v_grids.append(element_id)
    elif Grid_orientation != 1 and Grid_orientation != -1:
        h_grids.append(element_id)

# Get outline grids

# 1) get coordinates of grids

x_coordinates = []
y_coordinates = []

# 1.1) Get xmin, xmax

for element_ids in v_grids:
    Grid = doc.GetElement(element_ids)
    Grid_x = Grid.Curve.Origin.X
    # print(Grid_x)
    # print('*'*50)
    x_coordinates.append(Grid_x)


xmin = find_minimum_value(x_coordinates)
xmax = find_maximum_value(x_coordinates)
print(xmin)
print(xmax)
print('*'*50)

for element_ids in h_grids:
    Grid = doc.GetElement(element_ids)
    Grid_y = Grid.Curve.Origin.Y
    # print(Grid_y)
    # print('*'*50)
    y_coordinates.append(Grid_y)


ymin = find_minimum_value(y_coordinates)
ymax = find_maximum_value(y_coordinates)
print(ymin)
print(ymax)
print('*'*50)

# 1.2) Get corresponding grid to min/max coordinates

grid_id_xmin = v_grids[x_coordinates.index(xmin)]
grid_id_xmax = v_grids[x_coordinates.index(xmax)]

print("Element ID corresponding to leftmost grid:", grid_id_xmin)
print("Element ID corresponding to rightmost grid:", grid_id_xmax)

grid_id_ymin = h_grids[y_coordinates.index(ymin)]
grid_id_ymax = h_grids[y_coordinates.index(ymax)]

print("Element ID corresponding to lowermost grid:", grid_id_ymin)
print("Element ID corresponding to uppermost grid:", grid_id_ymax)
