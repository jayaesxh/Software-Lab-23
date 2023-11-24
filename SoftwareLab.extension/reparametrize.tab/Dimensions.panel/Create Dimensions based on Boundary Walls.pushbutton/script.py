# -*- coding: utf-8 -*-
__title__ = "Create Dimensions based on Outer Grids"
__doc__ = """______"""

# IMPORTS
# ==================================================
# Regular + Autodesk

import sys

import json
import math
import System
import clr
import re
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

def mm_to_feet(mm_value):
    # 1 mm is approximately 0.00328084 feet
    feet_value = mm_value * 0.00328084
    return feet_value

def feet_to_mm(feet_value):
    # 1 foot is approximately 304.8 millimeters
    mm_value = feet_value * 304.8
    return mm_value


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

    return (element_ids_int)

def drive_selected_dimensions(document, name, value, dimset):
    if not GlobalParametersManager.AreGlobalParametersAllowed(document):
        raise ValueError("Global parameters are not permitted in the given document")

    if not GlobalParametersManager.IsUniqueName(document, name):
        raise ValueError("Global parameter with such name already exists in the document")

    if value <= 0.0:
        raise ValueError("Value of a global parameter that drives dimension must be a positive number")

    n_labeled_dims = 0  # number of labeled dimensions (for testing)

    # creation of any element must be in a transaction
    with Transaction(document, "Create Global Parameter") as trans:
        trans.Start()

        # create a GP with the given name and type Length
        # Note: Length (or Angle) is required type of global parameters that are to label a dimension
        newgp = GlobalParameter.Create(document, name, SpecTypeId.Length)
        if newgp is not None:
            newgp.SetValue(DoubleParameterValue(value))

            # use the parameter to label the given dimensions
            for elemid in dimset:
                # not just any dimension is allowed to be labeled
                # check first to avoid exceptions
                elemid_ = (doc.GetElement(ElementId(elemid))).Id
                if newgp.CanLabelDimension(elemid_):
                    newgp.LabelDimension(elemid_)
                    n_labeled_dims += 1

            trans.Commit()

def create_new_labelled_global_parameter(document, name, value):
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

# VARIABLES
# ==================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel
rvt_year = int(app.VersionNumber)


# MAIN
# ==================================================

# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictA, 'r') as file:
    dictA = json.load(file)

print(dictA)
print("Type dictA: ", type(dictA))

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

outline_grids = []
outline_grids.append(grid_id_xmin)
outline_grids.append(grid_id_xmax)
outline_grids.append(grid_id_ymin)
outline_grids.append(grid_id_ymax)

outline_grids_int = extract_element_ids(outline_grids)
print(outline_grids_int)
print('*' * 50)

left_grid = outline_grids_int[0]
right_grid = outline_grids_int[1]
up_grid = outline_grids_int[3]
down_grid = outline_grids_int[2]

# WALL SORTING
v_walls = []
h_walls = []
for wall_id, grid_id in dictA.items():
    # Perform operations on each element ID here

    wall = doc.GetElement(ElementId(int(wall_id)))

    wall_orientation = wall.Location.Curve.Direction.Y
    if wall_orientation == 1 or wall_orientation == -1:
        v_walls.append(wall_id)
    elif wall_orientation != 1 or wall_orientation != -1:
        h_walls.append(wall_id)

print(v_walls)
print("Vertical Wall IDs: {}".format(';'.join(v_walls)))
print(h_walls)
print("Horizontal Wall IDs: {}".format(';'.join(h_walls)))

tol = app.ShortCurveTolerance

dict_LG_VW = {left_grid: v_walls}           #LG = left grid, RG = right grid, UG = up grid, DG = down grid
dict_RG_VW = {right_grid: v_walls}          #VW = vert wall, HW = hor wall
dict_UG_HW = {up_grid: h_walls}
dict_DG_HW = {down_grid: h_walls}

dict_VW_LD = {}
dim_LD = []
dict_HW_DD = {}
dim_DD = []

print(dict_LG_VW)

# VERTICAL WALLS

# VERTICAL WALLS - LEFT GRID


for wall_id in v_walls:
    # Get Wall and Grid elements based on their IDs

    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(left_grid)))

    wep0 = wall.Location.Curve.GetEndPoint(0)
    wep1 = wall.Location.Curve.GetEndPoint(1)
    # print('Wall End Pt 0 (for Wall ID - {}): {}'.format(wall_id, wep0))
    # print('Wall End Pt 1 (for Wall ID - {}): {}'.format(wall_id, wep1))
    print('*' * 50)

    gep0 = grid.Curve.GetEndPoint(0)
    gep1 = grid.Curve.GetEndPoint(1)
    # print('Grid End Pt 0 (for Grid ID - {}): {}'.format(grid_id, gep0))
    # print('Grid End Pt 1 (for Grid ID - {}): {}'.format(grid_id, gep1))
    print('*' * 50)

    # Create dimensions between Wall and Grid
    start = XYZ(wep0[0], wep0[1] - 5, 0)
    end = XYZ((gep1[0] + 2 * tol), wep0[1] - 5, 0)

    # # Calculate the difference between start and end
    # difference = (end - start).GetLength()
    # print("Difference between wall {} and grid {} is {}.".format(wall_id, grid_id, difference))

    t = Transaction(doc, 'Create Dimension')
    t.Start()

    lines = Line.CreateBound(start, end)

    # CREATE REFERENCE ARRAY
    refArray = ReferenceArray()
    refArray.Append(Reference(wall))
    refArray.Append(Reference(grid))

    # CREATE NEW DIMENSION
    dim = doc.Create.NewDimension(active_view, lines, refArray)
    t.Commit()

    dim_id = dim.Id.IntegerValue
    dim_LD.append(dim_id)
    dict_VW_LD[wall_id] = dim_id

    print("Created Horizontal Dimension Successfully between wall {} and grid {}.".format(wall_id, grid_id))
else:
    print("No Horizontal Dimension Created between wall {} and grid {} due to tolerance.".format(wall_id, grid_id))

print(dict_VW_LD)
print(dim_LD)

for wall_id, dim_id in dict_VW_LD.items():
    gp_name = "Distance_Left_Grid_and_Wall_ID_{}".format(int(wall_id))  # Adding 1 to make the index 1-based
    dim = doc.GetElement((ElementId(int(dim_id))))
    dim_value = dim.Value
    print(feet_to_mm(dim_value))

    global_parameter_id = create_new_labelled_global_parameter(doc, gp_name, dim_value)

    # Label Dimension
    t = Transaction(doc, 'Label Dimension')
    t.Start()

    gp = doc.GetElement(global_parameter_id)
    label = gp.LabelDimension(ElementId(dim_id))

    t.Commit()
    print("Labeled Dimension Successfully")


# HORIZONTAL WALLS

# HORIZONTAL WALLS - LOWER GRID


for wall_id in h_walls:
    # Get Wall and Grid elements based on their IDs

    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(down_grid)))

    wep0 = wall.Location.Curve.GetEndPoint(0)
    wep1 = wall.Location.Curve.GetEndPoint(1)
    # print('Wall End Pt 0 (for Wall ID - {}): {}'.format(wall_id, wep0))
    # print('Wall End Pt 1 (for Wall ID - {}): {}'.format(wall_id, wep1))
    print('*' * 50)

    gep0 = grid.Curve.GetEndPoint(0)
    gep1 = grid.Curve.GetEndPoint(1)
    # print('Grid End Pt 0 (for Grid ID - {}): {}'.format(grid_id, gep0))
    # print('Grid End Pt 1 (for Grid ID - {}): {}'.format(grid_id, gep1))
    print('*' * 50)

    # Create dimensions between Wall and Grid
    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep0[0], (gep0[1] + 2 * tol), 0)

    # # Calculate the difference between start and end
    # difference = (end - start).GetLength()
    # print("Difference between wall {} and grid {} is {}.".format(wall_id, grid_id, difference))

    t = Transaction(doc, 'Create Dimension')
    t.Start()

    lines = Line.CreateBound(start, end)

    # CREATE REFERENCE ARRAY
    refArray = ReferenceArray()
    refArray.Append(Reference(wall))
    refArray.Append(Reference(grid))

    # CREATE NEW DIMENSION
    dim = doc.Create.NewDimension(active_view, lines, refArray)
    t.Commit()

    dim_id = dim.Id.IntegerValue
    dim_DD.append(dim_id)
    dict_HW_DD[wall_id] = dim_id

    print("Created Vertical Dimension Successfully between wall {} and grid {}.".format(wall_id, grid_id))
else:
    print("No Vertical Dimension Created between wall {} and grid {} due to tolerance.".format(wall_id, grid_id))

print(dict_HW_DD)
print(dim_DD)

for wall_id, dim_id in dict_HW_DD.items():
    gp_name = "Distance_Lower_Grid_and_Wall_ID_{}".format(int(wall_id))
    dim = doc.GetElement((ElementId(int(dim_id))))
    dim_value = dim.Value
    print(feet_to_mm(dim_value))

    global_parameter_id = create_new_labelled_global_parameter(doc, gp_name, dim_value)

    # Label Dimension
    t = Transaction(doc, 'Label Dimension')
    t.Start()

    gp = doc.GetElement(global_parameter_id)
    label = gp.LabelDimension(ElementId(dim_id))

    t.Commit()
    print("Labeled Dimension Successfully")