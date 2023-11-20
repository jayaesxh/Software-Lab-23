# -*- coding: utf-8 -*-
__title__ = "Create Dictionary"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk

import json

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

import re
import sys
import math
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

# pyRevit
from pyrevit import forms, revit

# VARIABLES
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


def get_coordinates(element):
    curve = element.Location.Curve
    return curve.Origin.X, curve.Origin.Y


def calculate_distance(wall_value, grid_value):
    return abs(wall_value - grid_value)


def feet_to_mm(feet_value):
    # Assuming you have a function to convert feet to mm
    return feet_value


def get_orientation(element):
    return abs(element.Location.Curve.Direction.Y)


def process_grids(grids, orientation, wall_value, wall_orientation):
    distances = []
    for grid_id in grids:
        grid = doc.GetElement(grid_id)
        grid_value = feet_to_mm(get_coordinates(grid)[0 if orientation == 1 else 1])
        distance = calculate_distance(wall_value, grid_value)
        distances.append(distance)

    return find_minimum_value(distances)


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


# MAIN
# ==================================================


# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictA, 'r') as file:
    dictA = json.load(file)

print(dictA)
print("Type dictA: ", type(dictA))

wall_element_ids = []


def mm_to_feet(mm):
    # 1 millimeter is equal to 0.00328084 feet
    feet = mm * 0.00328084
    return feet


parameter_id = []
all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)

for p_id in all_global_parameter_ids:
    p = doc.GetElement(p_id)
    # print('GP Name: {}; ID: {}'.format(p.Name, p_id))
    parameter_id.append(p_id)

parameter_id_int = extract_element_ids(parameter_id)
print(parameter_id_int)

wall_element_ids = list(dictA.keys())
print("wall_element_ids", wall_element_ids)

dictB = {}
for k, v in zip(wall_element_ids, parameter_id_int):
    dictB[k] = v
print(dictB)

# Convert both keys and values to strings in the dictionary
dictB_str = {str(key): str(value) for key, value in dictB.items()}

file_path_dictB = r'C:\Users\harsh\OneDrive\Documents\newew\dictB.json'

with open(file_path_dictB, 'w') as fp:  # insert file path here
    json.dump(dictB_str, fp, indent=4)

print("JSON file created successfully.")
