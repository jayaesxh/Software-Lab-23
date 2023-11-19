# -*- coding: utf-8 -*-
__title__ = "Create/Label Dimensions"
__author__ = "Jayesh_Bhadva"
__version__ = "Version 1.0"
__doc__ = """ Description:  """

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction, Line, XYZ
from pyrevit import revit, DB
# .NET IMPORTS
import clr
import json
import re

clr.AddReference('System')
from System.Collections.Generic import List

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# ====================================================================================================
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

active_view = doc.ActiveView
active_level = doc.ActiveView.GenLevel


def feet_to_mm(feet):
    # 1 foot = 304.8 millimeters
    mm = feet * 304.8
    return mm


def create_new_dimension_along_line(document, line):
    # Use the Start and End points of our line as the references
    # Line must come from something in Revit, such as a beam
    references = []
    references.append(line.GetEndPointReference(0))
    references.append(line.GetEndPointReference(1))
    # create the new dimension
    dimension = document.Create.NewDimension(document.ActiveView, line, references)
    return dimension


def extract_element_ids(element_ids):
    # Convert ElementId objects to string representation
    element_ids_str = str(element_ids)

    # Extract element IDs between square brackets using regular expression
    extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)

    # Convert the extracted strings to integers
    element_ids_int = [int(id_str) for id_str in extracted_ids]

    return element_ids_int

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ====================================================================================================

# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictA, 'r') as file:
    dictA = json.load(file)

print(dictA)
print("Type dictA: ", type(dictA))

# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictB = r'C:\Users\harsh\OneDrive\Documents\newew\dictB.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictB, 'r') as file:
    dictB = json.load(file)

print(dictB)
print("Type dictA: ", type(dictB))

tol = app.ShortCurveTolerance

# GRID SORTING
v_grids = []
h_grids = []
for wall_id, grid_id in dictA.items():
    # Perform operations on each element ID here

    grid = doc.GetElement(ElementId(int(grid_id)))

    Grid_orientation = grid.Curve.Direction.Y
    if Grid_orientation == -1:
        grid_o = "V"
        v_grids.append(grid_id)
    elif Grid_orientation != -1:
        grid_o = "H"
        h_grids.append(grid_id)


# MAKE dictA SEPARATE FOR HORIZONTAL AND VERTICAL WALLS/GRIDS

dictA_hor_dim = {}
dictA_ver_dim = {}

for wall_id, grid_id in dictA.items():
    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(grid_id)))

    # Check if the orientations match
    if wall.Location.Curve.Direction.Y == -1 or wall.Location.Curve.Direction.Y == 1 and grid.Curve.Direction.Y == -1 or grid.Curve.Direction.Y == 1:
        # For vertical grids
        dictA_hor_dim[wall_id] = grid_id
    elif wall.Location.Curve.Direction.Y != -1 or wall.Location.Curve.Direction.Y != 1 and grid.Curve.Direction.Y != -1 or grid.Curve.Direction.Y != 1:
        # For horizontal grids
        dictA_ver_dim[wall_id] = grid_id

# Print horizontal dimension dictionary
print("Following are Vertical Walls/Grids for Horizontal Dimensions:")
print(";".join("{};{}".format(key, value) for key, value in dictA_hor_dim.items()))

# Print vertical dimension dictionary
print("Following are Horizontal Walls/Grids for Vertical Dimensions:")
print(";".join("{};{}".format(key, value) for key, value in dictA_ver_dim.items()))


dictC_hor_dim = {}  #key = wall_id & value = dim_id
dictC_ver_dim = {}

dictD_hor_dim = {}  #key = GP_id & value = dim_id
dictD_ver_dim = {}

# HORIZONTAL DIMENSIONS

for wall_id, grid_id in dictA_hor_dim.items():
    # Get Wall and Grid elements based on their IDs
    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(grid_id)))

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

    # Calculate the difference between start and end
    difference = (end - start).GetLength()
    print("Difference between wall {} and grid {} is {}.".format(wall_id, grid_id, difference))

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

    dictC_hor_dim[wall_id] = dim_id

    print("Created Horizontal Dimension Successfully between wall {} and grid {}.".format(wall_id, grid_id))
else:
    print("No Horizontal Dimension Created between wall {} and grid {} due to tolerance.".format(wall_id, grid_id))

print(dictC_hor_dim)
print(";".join("{};{}".format(key, value) for key, value in dictC_hor_dim.items()))

for wall_id_B, gp_id in dictB.items():
    for wall_id_C, dim_id_wall in dictC_hor_dim.items():
        # Compare keys from dictB and dictC_hor_dim
        if wall_id_B == wall_id_C:
            dictD_hor_dim[gp_id] = dim_id_wall

print(dictD_hor_dim)
print(";".join("{};{}".format(key, value) for key, value in dictD_hor_dim.items()))

# LABEL HORIZONTAL DIMENSIONS

for gp_id, dim_id in dictD_hor_dim.items():
    t = Transaction(doc, 'Label Dimension')
    t.Start()

    print("Labelling Horizontal Dimension with GP {} on Dimension {}.".format(gp_id, dim_id))

    gp = doc.GetElement(ElementId(int(gp_id)))  #GP_ID

    label = gp.LabelDimension((ElementId(int(dim_id)))) #Dim_ID

    t.Commit()
    print("Labeled Horizontal Dimension Successfully")

# VERTICAL DIMENSIONS

for wall_id, grid_id in dictA_ver_dim.items():
    # Get Wall and Grid elements based on their IDs
    wall = doc.GetElement(ElementId(int(wall_id)))
    grid = doc.GetElement(ElementId(int(grid_id)))

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
    start = XYZ(wep0[0] - 5, wep0[1], 0)
    end = XYZ(wep0[0], (gep0[1] + 2 * tol), 0)

    # Calculate the difference between start and end
    difference = (end - start).GetLength()
    print("Difference between wall {} and grid {} is {}.".format(wall_id, grid_id, difference))

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

    dictC_ver_dim[wall_id] = dim_id

    print("Created Vertical Dimension Successfully between wall {} and grid {}.".format(wall_id, grid_id))
else:
    print("No Vertical Dimension Created between wall {} and grid {} due to tolerance.".format(wall_id, grid_id))

print(dictC_ver_dim)
print(";".join("{};{}".format(key, value) for key, value in dictC_ver_dim.items()))

for wall_id_B, gp_id in dictB.items():
    for wall_id_C, dim_id_wall in dictC_ver_dim.items():
        # Compare keys from dictB and dictC_ver_dim
        if wall_id_B == wall_id_C:
            dictD_ver_dim[gp_id] = dim_id_wall

print(dictD_ver_dim)
print(";".join("{};{}".format(key, value) for key, value in dictD_ver_dim.items()))

# LABEL VERTICAL DIMENSIONS

for gp_id, dim_id in dictD_ver_dim.items():
    t = Transaction(doc, 'Label Dimension')
    t.Start()

    print("Labelling Vertical Dimension with GP {} on Dimension {}.".format(gp_id, dim_id))

    gp = doc.GetElement(ElementId(int(gp_id)))  #GP_ID

    label = gp.LabelDimension((ElementId(int(dim_id)))) #Dim_ID

    t.Commit()
    print("Labeled Vertical Dimension Successfully")
