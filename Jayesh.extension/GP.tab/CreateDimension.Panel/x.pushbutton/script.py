# -*- coding: utf-8 -*-
__title__ = "z"
__author__ = "Jayesh"
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


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ====================================================================================================

# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictA = r'C:\Users\jayes\Desktop\Revit Extensions\dictA.json' 

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictA, 'r') as file:
    dictA = json.load(file)

print(dictA)
print("Type dictA: ", type(dictA))

# Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
file_path_dictB = r'C:\Users\jayes\Desktop\Revit Extensions\dictB.json'

# Open the JSON file and load its contents into a dictionary
with open(file_path_dictB, 'r') as file:
    dictB = json.load(file)

print(dictB)
print("Type dictA: ", type(dictB))

# GRID SORTING
v_grids = []
h_grids = []
for wall_id, grid_id in dictA.items():
    # Perform operations on each element ID here

    Grid = doc.GetElement(ElementId(int(grid_id)))

    Grid_orientation = Grid.Curve.Direction.Y # Grid not GridType.
    if Grid_orientation == -1:
        grid_o = "V"
        v_grids.append(grid_id)
    elif Grid_orientation != -1:
        grid_o = "H"
        h_grids.append(grid_id)


# HORIZONTAL DIMENSIONS

for wall_id, grid_id in dictA.items():
    # Get Wall and Grid elements based on their IDs
    Wall = doc.GetElement(ElementId(int(wall_id)))
    Grid = doc.GetElement(ElementId(int(grid_id)))

    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)
    print('Wall End Pt 0 (for Wall ID - {}): {}'.format(wall_id, wep0))
    print('Wall End Pt 1 (for Wall ID - {}): {}'.format(wall_id, wep1))
    print('*' * 50)

    gep0 = Grid.Curve.GetEndPoint(0)
    gep1 = Grid.Curve.GetEndPoint(1)
    print('Grid End Pt 0 (for Grid ID - {}): {}'.format(grid_id, gep0))
    print('Grid End Pt 1 (for Grid ID - {}): {}'.format(grid_id, gep1))
    print('*' * 50)

    # Check if the orientations match
    if Wall.Location.Curve.Direction.Y == -1 or Wall.Location.Curve.Direction.Y == 1 and Grid.Curve.Direction.Y == -1 or Grid.Curve.Direction.Y == 1:
        # Both are vertical grids
        v_grids.append(grid_id)
    elif Wall.Location.Curve.Direction.Y != -1 or Wall.Location.Curve.Direction.Y != 1 and Grid.Curve.Direction.Y != -1 or Grid.Curve.Direction.Y != 1:
        # Both are horizontal grids
        h_grids.append(grid_id)

    # Create dimensions between Wall and Grid
    start = XYZ(wep0[0], wep0[1] - 5, 0)
    end = XYZ(gep1[0], wep0[1] - 5, 0)

    # Calculate the difference between start and end
    difference = (end - start).GetLength()
    print("Difference between Wall {} and Grid {} is {}.".format(wall_id, grid_id, difference))

    t = Transaction(doc, 'Create Dimension')
    t.Start()

    lines = Line.CreateBound(start, end)

    # CREATE REFERENCE ARRAY
    refArray = ReferenceArray()
    refArray.Append(Reference(Wall))
    refArray.Append(Reference(Grid))

    # CREATE NEW DIMENSION
    doc.Create.NewDimension(active_view, lines, refArray)
    t.Commit()
    print("Created Horizontal Dimension Successfully between Wall {} and Grid {}.".format(wall_id, grid_id))
else:
    print("No Horizontal Dimension Created between Wall {} and Grid {} due to tolerance.".format(wall_id, grid_id))

# # VERTICAL DIMENSIONS

# for Wall, wall_tuple in wall_data.items():
#     wep0, wep1 = wall_tuple
#     for Grid, gep1 in grid_data.items():
#         start = XYZ(wep0[0] - 5, wep0[1], 0)  # Vertical dimension starts from the wall's top endpoint
#         end = XYZ(wep0[0] - 5, gep1[1], 0)  # Vertical dimension ends at the grid's Y-coordinate

#         # Calculate the difference between start and end
#         difference = (end - start).GetLength()

#         # Check if the difference is greater than or equal to 0.01
#         if difference >= 0.01:
#             t = Transaction(doc, 'Create Vertical Dimension')
#             t.Start()

#             lines = Line.CreateBound(start, end)

#             # CREATE REFERENCE ARRAY
#             refArray = ReferenceArray()
#             refArray.Append(Reference(Wall))
#             refArray.Append(Reference(Grid))

#             # CREATE NEW DIMENSION
#             doc.Create.NewDimension(active_view, lines, refArray)
#             t.Commit()
#             print("Created Vertical Dimension Successfully between Wall and Grid.")
#         else:
#             print("No Vertical Dimension Created between Wall and Grid due to tolerance.")

