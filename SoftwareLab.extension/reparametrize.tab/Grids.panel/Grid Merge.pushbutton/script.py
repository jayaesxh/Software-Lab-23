# -*- coding: utf-8 -*-
__title__ = "Grid Merge"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk

import clr
import re
# clr.AddReference('RevitAPI')
# clr.AddReference('RevitAPIUI')

import sys
import math

from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.__init___parts.DoubleParameterValue import DoubleParameterValue
# from Autodesk.Revit.DB.__init___parts.GlobalParameter import GlobalParameter
# from Autodesk.Revit.DB.__init___parts.ParameterType import ParameterType
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

from pyrevit import revit, forms

from Autodesk.Revit.DB import ElementId, GlobalParameter, DoubleParameterValue
from Autodesk.Revit.UI import TaskDialog
from System import InvalidOperationException, ArgumentException
from System.Collections.Generic import HashSet

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

import sys
import math
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId, Line, Grid

# pyRevit
from pyrevit import forms, revit

#VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
rvt_year = int(app.VersionNumber)

# CLASSES
# ==================================================

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

def extract_element_ids(element_ids):
    # Convert ElementId objects to string representation
    element_ids_str = str(element_ids)

    # Extract element IDs between square brackets using regular expression
    extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)

    # Convert the extracted strings to integers
    element_ids_int = [int(id_str) for id_str in extracted_ids]

    return element_ids_int

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

# Group grids based on their orientation (vertical/horizontal)
vertical_grids = []
horizontal_grids = []

x_coordinates = []
y_coordinates = []

x_coordinates_grid_id = {}
y_coordinates_grid_id = {}

for element_id in all_grids:
    Grid = doc.GetElement(element_id)
    Grid_orientation = Grid.Curve.Direction.Y
    if Grid_orientation == 1 or Grid_orientation == -1:
        vertical_grids.append(element_id)
    elif Grid_orientation != 1 and Grid_orientation != -1:
        horizontal_grids.append(element_id)

# print(extract_element_ids(vertical_grids))
# print(extract_element_ids(horizontal_grids))


# Get X-coordinates of vertical grids
for element_id in vertical_grids:
    grid = doc.GetElement(element_id)
    grid_x = grid.Curve.Origin.X
    x_coordinates.append(grid_x)
print("x_coordinates: {}".format(x_coordinates))

# Get Y-coordinates of horizontal grids
for element_id in horizontal_grids:
    grid = doc.GetElement(element_id)
    grid_y = grid.Curve.Origin.Y
    y_coordinates.append(grid_y)
print("y_coordinates: {}".format(y_coordinates))

# Check if X-coordinates of two consecutive grids are almost the same
for i in range(len(x_coordinates) - 1):
    current_x = x_coordinates[i]

    # Iterate over all other x_coordinates
    for j in range(i + 1, len(x_coordinates)):
        other_x = x_coordinates[j]

        # Define a tolerance value for considering X-coordinates as almost the same
        tolerance = 0.01  # You may adjust this value based on your requirements

        # Check if the absolute difference between X-coordinates is within the tolerance
        if abs(other_x - current_x) < tolerance:
            print('Grids {} and {} have almost the same X-coordinate.'.format(i + 1, j + 1))

            # Get the element IDs of the collinear grids
            start_point_id = vertical_grids[i]
            end_point_id = vertical_grids[j]

            # Get the grid elements from the element IDs
            start_point = doc.GetElement(start_point_id)
            end_point = doc.GetElement(end_point_id)

            # Get the start and end points of the collinear grids
            sp = start_point.Curve.GetEndPoint(0)
            ep = end_point.Curve.GetEndPoint(1)

            # Convert start and end points to XYZ objects
            start = XYZ(sp.X, sp.Y, 0)
            end = XYZ(ep.X, ep.Y, 0)

            # Start a transaction to delete old grids and create a merged grid
            t = Transaction(doc, 'Delete old Grid and create merged grid')
            t.Start()

            # Create a new line representing the merged grid
            geom_line = Line.CreateBound(start, end)

            # Create a new grid at the merged line
            merged_grid = Grid.Create(doc, geom_line)

            # Delete the old collinear grids
            doc.Delete(start_point_id)
            doc.Delete(end_point_id)

            t.Commit()
            print("Created Merged Grid Successfully")


# Check if Y-coordinates of two consecutive grids are almost the same
for i in range(len(y_coordinates) - 1):
    current_y = y_coordinates[i]
    # Iterate over all other y_coordinates
    for j in range(i + 1, len(y_coordinates)):
        other_y = y_coordinates[j]

        # Define a tolerance value for considering X-coordinates as almost the same
        tolerance = 0.01  # You may adjust this value based on your requirements

        # Check if the absolute difference between X-coordinates is within the tolerance
        if abs(other_y - current_y) < tolerance:
            print('Grids {} and {} have almost the same Y-coordinate.'.format(i + 1, j + 1))

            # Get the element IDs of the collinear grids
            start_point_id = horizontal_grids[i]
            end_point_id = horizontal_grids[j]

            # Get the grid elements from the element IDs
            start_point = doc.GetElement(start_point_id)
            end_point = doc.GetElement(end_point_id)

            # Get the start and end points of the collinear grids
            sp = start_point.Curve.GetEndPoint(0)
            ep = end_point.Curve.GetEndPoint(1)

            # Convert start and end points to XYZ objects
            start = XYZ(sp.X, sp.Y, 0)
            end = XYZ(ep.X, ep.Y, 0)

            # Start a transaction to delete old grids and create a merged grid
            t = Transaction(doc, 'Delete old Grid and create merged grid')
            t.Start()

            # Create a new line representing the merged grid
            geom_line = Line.CreateBound(start, end)

            # Create a new grid at the merged line
            merged_grid = Grid.Create(doc, geom_line)

            # Delete the old collinear grids
            doc.Delete(start_point_id)
            doc.Delete(end_point_id)

            t.Commit()
            print("Created Merged Grid Successfully")
