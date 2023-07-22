# -*- coding: utf-8 -*-
__title__ = "Wall-Grid Distance"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk

import clr
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
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

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
def feet_to_mm(feet):
    inches = feet * 12
    mm = inches * 25.4
    return mm

def mm_to_feet(mm):
    # 1 millimeter is equal to 0.00328084 feet
    feet = mm * 0.00328084
    return feet

def calculate_distance(point1, point2):
    distance = abs(point2 - point1)
    return distance


def find_minimum_value(values):
    min_value = float('inf')  # Initialize with a large value

    for value in values:
        if value < min_value:
            min_value = value

    return min_value


def find_second_least_value(numbers):
    # Ensure that the list is not empty and has at least two elements
    if len(numbers) < 2:
        raise ValueError("The list must have at least two elements to find the second least value.")

    # Initialize min_value and second_min_value with the first two elements
    min_value, second_min_value = float('inf'), float('inf')

    # Iterate through the list to find the two minimum values
    for num in numbers:
        if num < min_value:
            second_min_value = min_value
            min_value = num
        elif num < second_min_value and num != min_value:
            second_min_value = num

    # Check if a second least value was found
    if second_min_value == float('inf'):
        raise ValueError("There is no second least value in the list.")

    return second_min_value

# MAIN
# ==================================================


# GET ALL WALLS
all_walls = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
print(all_walls)

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

# GET DISTANCE BETWEEN WALL AND GRID

# 1) get wall coordinate and orientation

wall_element_ids = []
min_distances = []

for element_id in all_walls:
    Wall = doc.GetElement(element_id)

    Wall_x = Wall.Location.Curve.Origin.X
    print('Wall_p1 for Element ID- {}: {}'.format(element_id, Wall_x))
    Wall_y = Wall.Location.Curve.Origin.Y
    print('Wall_p2 for Element ID- {}: {}'.format(element_id, Wall_y))

    Wall_orientation = abs(Wall.Location.Curve.Direction.Y)                          # V==1 & H!=1
    print('Wall_orientation for Element ID- {}: {}'.format(element_id, Wall_orientation))

# 2) get coordinates of grids (which are parallel to wall)

    distance_grids = []

    if Wall_orientation == 1:
        for element_ids in v_grids:
            Grid = doc.GetElement(element_ids)
            Grid_x = Grid.Curve.Origin.X
            Grid_y = Grid.Curve.Origin.Y

            Wall_mm_value = feet_to_mm(Wall_x)
            Grid_mm_value = feet_to_mm(Grid_x)

            distance = calculate_distance(Wall_mm_value, Grid_mm_value)
            print('Distance(hor) for Element ID- {}: {}'.format(element_ids, distance))

            distance_grids.append(distance)

    elif Wall_orientation != 1:
        for element_ids in h_grids:
            Grid = doc.GetElement(element_ids)
            Grid_x = Grid.Curve.Origin.X
            Grid_y = Grid.Curve.Origin.Y

            Wall_mm_value = feet_to_mm(Wall_y)
            Grid_mm_value = feet_to_mm(Grid_y)

            distance = calculate_distance(Wall_mm_value, Grid_mm_value)
            print('Distance(ver) for Element ID- {}: {}'.format(element_ids, distance))

            distance_grids.append(distance)

    threshold = 0.00001
    xmin = find_minimum_value(distance_grids)
    x2min = find_second_least_value(distance_grids)

    if xmin > threshold:
        min_distance = xmin
    elif xmin < threshold:
        min_distance = x2min

    print('min_distance for Element ID- {}: {}'.format(element_id, min_distance))
    print('*' * 50)

    wall_element_ids.append(element_id)
    min_distances.append(min_distance)

print('*' * 50)
# Creating the dictionary using a loop
min_distance_dict = {}
for i in range(len(wall_element_ids)):
    element_id = wall_element_ids[i]
    min_distance = min_distances[i]
    min_distance_dict[element_id] = min_distance

# Printing the created dictionary
print(min_distance_dict)

#CREATE GP AND SET IT WITH PREVIOUS VALUE

def create_new_global_parameter(document, name, value):
    if not GlobalParametersManager.AreGlobalParametersAllowed(document):
        raise System.InvalidOperationException("Global parameters are not permitted in the given document")
    if not GlobalParametersManager.IsUniqueName(document, name):
        raise System.ArgumentException("Global parameter with such name already exists in the document", "name")
    gpid = ElementId.InvalidElementId
    # creation of any element must be in a transaction
    with Transaction(document, "Create Global Parameter") as trans:
        trans.Start()
        # create a GP with the given name and type Length
        gp = GlobalParameter.Create(document, name, SpecTypeId.Length)
        if gp is not None:
            # if created successfully, assign it a value
            # note: parameters of type Length accept Double values
            gp.SetValue(DoubleParameterValue(value))
            gpid = gp.Id
        trans.Commit()
    return gpid

def mm_to_feet(mm):
    # 1 millimeter is equal to 0.00328084 feet
    feet = mm * 0.00328084
    return feet

for x,y in min_distance_dict.items():

    parameter_name = 'Closest_Distance_EID_{}'.format(x)
    parameter_value = mm_to_feet(y)

    # Call the function to create the new global parameter
    global_parameter_id = create_new_global_parameter(doc, parameter_name, parameter_value)

    # Print the ID of the created global parameter
    print("Created Global Parameter ID:", global_parameter_id)
