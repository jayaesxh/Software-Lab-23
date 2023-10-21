# -*- coding: utf-8 -*-
__title__ = "Automated Parameter Creation"
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


# MAIN
# ==================================================


# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
json_file_path = r'C:\Users\harsh\OneDrive\Documents\newew\file1.json'

# Open the JSON file and load its contents into a dictionary
with open(json_file_path, 'r') as file:
    dictA = json.load(file)

wall_element_ids = []

all_walls = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()

all_grids = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()

for element_id in all_walls:
    Wall = doc.GetElement(element_id)
    # print('Wall Element ID- {}'.format(element_id))
    wall_element_ids.append(element_id)
print(wall_element_ids)
print('*' * 50)

wall_element_ids_int = extract_element_ids(wall_element_ids)
print(wall_element_ids_int)

number_of_parameters = len(wall_element_ids)


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


for i in range(number_of_parameters):
    parameter_name = 'Distance_Parameter_{}'.format(i + 1)
    parameter_value = 0.0

    # Call the function to create the new global parameter
    global_parameter_id = create_new_global_parameter(doc, parameter_name, parameter_value)

    # Print the ID of the created global parameter
    print("Created Global Parameter ID:", global_parameter_id)

parameter_id = []
all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)

for p_id in all_global_parameter_ids:
    p = doc.GetElement(p_id)
    # print('GP Name: {}; ID: {}'.format(p.Name, p_id))
    parameter_id.append(p_id)

parameter_id_int = extract_element_ids(parameter_id)
print(parameter_id_int)

dictB = {}
for k, v in zip(wall_element_ids_int, parameter_id_int):
    dictB[k] = v
print(dictB)

with open(r'C:\Users\harsh\OneDrive\Documents\newew\dictB.json', 'w') as fp:        #insert file path here
    json.dump(dictB, fp, indent=4)

print("JSON file created successfully.")
