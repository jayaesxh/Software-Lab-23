# -*- coding: utf-8 -*-
__title__ = "CREATE DICTIONARY"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk
#
import re
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

import sys
import math
import json

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
import os
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


def extract_element_ids_from_dict(input_dict):
    extracted_dict = {}

    for key, value in input_dict.items():
        # Extract numeric values from key
        extracted_key = int(re.search(r'\d+', str(key)).group()) if re.search(r'\d+', str(key)) else None

        # Extract numeric values from value
        extracted_value = int(re.search(r'\d+', str(value)).group()) if re.search(r'\d+', str(value)) else None

        # Update the dictionary with extracted key-value pair
        if extracted_key is not None and extracted_value is not None:
            extracted_dict[extracted_key] = extracted_value

    return extracted_dict

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



# GET ALL GRIDS

all_grids = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()
#print(all_grids)

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

# Initialize an empty dictionary to store the mapping
wall_to_grid_mapping = {}

for element_id in all_walls:
    Wall = doc.GetElement(element_id)

    Wall_orientation = abs(Wall.Location.Curve.Direction.Y)  # V==1 & H!=1

    min_distance = None
    closest_grid_id = None

    for grid_id in v_grids if Wall_orientation == 1 else h_grids:
        Grid = doc.GetElement(grid_id)
        Grid_x = Grid.Curve.Origin.X if Wall_orientation == 1 else Grid.Curve.Origin.Y
        Wall_coordinate = Wall.Location.Curve.Origin.X if Wall_orientation == 1 else Wall.Location.Curve.Origin.Y

        Wall_mm_value = feet_to_mm(Wall_coordinate)
        Grid_mm_value = feet_to_mm(Grid_x)

        distance = calculate_distance(Wall_mm_value, Grid_mm_value)

        if min_distance is None or distance < min_distance:
            min_distance = distance
            closest_grid_id = grid_id

    if closest_grid_id is not None:
        wall_to_grid_mapping[element_id] = closest_grid_id

# Now, wall_to_grid_mapping is a dictionary with wall element IDs as keys and closest grid element IDs as values
# print('*' * 50)
# print(wall_to_grid_mapping)
# print('*' * 50)

wall_to_grid_mapping_int = extract_element_ids_from_dict(wall_to_grid_mapping)
# print(wall_to_grid_mapping_int)

# Export the dictionary to a JSON file
# Ask the user for the file path
directory_path = r'D:\Software Lab Data\Revit_Plug-ins\Anurag.extension\testplugin.tab\Create Dictionary.panel\Create Dictionary.pushbutton'

file_name = 'output.json'

# Combining the directory path and file name to create the full file path
file_path = os.path.join(directory_path, file_name)
# Check if the provided file path is valid
if not file_path:
    print("Invalid file path")

else:
    with open(file_path, 'w') as json_file:
        json.dump(wall_to_grid_mapping_int, json_file, indent=4)
