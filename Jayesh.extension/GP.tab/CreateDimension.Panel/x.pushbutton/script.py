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
all_walls = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
# print(all_walls)
print('#' * 50)

# GET ALL GRIDS
all_grids = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()

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


# HORIZONTAL DIMENSIONS

wall_data = {}
for wall_id in all_walls:
    Wall = doc.GetElement(wall_id)
    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)
    print('Wall End Pt 0 (for Wall ID - {}): {}'.format(wall_id, wep0))
    print('Wall End Pt 1 (for Wall ID - {}): {}'.format(wall_id, wep1))
    print('*' * 50)

    # Create a tuple with wep0 and wep1 as values
    wall_tuple = (wep0, wep1)

    # Assign the tuple to the dictionary using wall_id as the key
    wall_data[Wall] = wall_tuple
# print('Wall Data Dictionary:')
# print(wall_data)

grid_data = {}
for grid_id in all_grids:
    Grid = doc.GetElement(grid_id)
    gep0 = Grid.Curve.GetEndPoint(0)
    gep1 = Grid.Curve.GetEndPoint(1)
    print('Grid End Pt 0 (for Grid ID - {}): {}'.format(grid_id, gep0))
    print('Grid End Pt 1 (for Grid ID - {}): {}'.format(grid_id, gep1))
    print('*' * 50)
    grid_data[Grid] = gep1
# print(grid_data)

for Wall, wall_tuple in wall_data.items():
    wep0, wep1 = wall_tuple
    for Grid, gep1 in grid_data.items():
        start = XYZ(wep0[0], wep0[1] - 5, 0)
        end = XYZ(gep1[0], wep0[1] - 5, 0)

        # Calculate the difference between start and end
        difference = (end - start).GetLength()

        # Check if the difference is greater than or equal to 0.01
        if difference >= 0.01:
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
            print("Created Horizontal Dimension Successfully between Wall and Grid.")
        else:
            print("No Horizontal Dimension Created between Wall and Grid due to tolerance.")

# VERTICAL DIMENSIONS

for Wall, wall_tuple in wall_data.items():
    wep0, wep1 = wall_tuple
    for Grid, gep1 in grid_data.items():
        start = XYZ(wep0[0] - 5, wep0[1], 0)  # Vertical dimension starts from the wall's top endpoint
        end = XYZ(wep0[0] - 5, gep1[1], 0)  # Vertical dimension ends at the grid's Y-coordinate

        # Calculate the difference between start and end
        difference = (end - start).GetLength()

        # Check if the difference is greater than or equal to 0.01
        if difference >= 0.01:
            t = Transaction(doc, 'Create Vertical Dimension')
            t.Start()

            lines = Line.CreateBound(start, end)

            # CREATE REFERENCE ARRAY
            refArray = ReferenceArray()
            refArray.Append(Reference(Wall))
            refArray.Append(Reference(Grid))

            # CREATE NEW DIMENSION
            doc.Create.NewDimension(active_view, lines, refArray)
            t.Commit()
            print("Created Vertical Dimension Successfully between Wall and Grid.")
        else:
            print("No Vertical Dimension Created between Wall and Grid due to tolerance.")

