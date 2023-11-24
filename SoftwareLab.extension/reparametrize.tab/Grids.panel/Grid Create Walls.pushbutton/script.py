# -*- coding: utf-8 -*-
#Practicing FilteredElementCollector

__title__ = "Create Wall-Grids"  # Name of button displayed in Revit API
__doc__ = """This is a simple tool to create grids"""


# """
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# """
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import forms

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Line, Grid, XYZ, ElementTransformUtils, BoundingBoxXYZ
from Autodesk.Revit.DB import Transaction
from pyrevit import revit, DB

# """
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
# """
doc     =__revit__.ActiveUIDocument.Document
uidoc   =__revit__.ActiveUIDocument
app     =__revit__.Application

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝

# FECs

# Creating grids using wall reference and setting up the particular grid length

# Get wall
# GET ALL WALLS
all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
all_grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()
all_columns = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
# print(list(all_columns))
# print(list(all_walls))
# print(list(all_grids))
# print('*' * 50)

# WALL ORIENTATION

v_walls = []
h_walls = []

for element_id in all_walls:
    Wall = doc.GetElement(element_id)

    Wall_x = Wall.Location.Curve.Origin.X
    # print('Wall_p1 for Element ID- {}: {}'.format(element_id, Wall_x))
    Wall_y = Wall.Location.Curve.Origin.Y
    # print('Wall_p2 for Element ID- {}: {}'.format(element_id, Wall_y))

    Wall_orientation = abs(Wall.Location.Curve.Direction.Y)                          # V==1 & H!=1
    # print('Wall_orientation for Element ID- {}: {}'.format(element_id, Wall_orientation))

    if Wall_orientation == 1:
        v_walls.append(element_id)
    elif Wall_orientation != 1:
        h_walls.append(element_id)

# print(v_walls)
# print('*'*50)
# print(h_walls)

#for vertical grids

wall_length_tolerance = 2.5  #2.5 feet = 0.75 meter

for element_id in v_walls:
    Wall = doc.GetElement(element_id)
    # print('Wall ID - {}'.format(element_id))

    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)
    # print('Wall End Pt 0 (for Wall ID - {}): {}'.format(element_id, wep0))
    # print('Wall End Pt 1 (for Wall ID - {}): {}'.format(element_id, wep1))
    print('*' * 100)

    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep1[0], wep1[1], 0)

    wall_length = start.DistanceTo(end)

    # print(start)
    # print(end)
    if wall_length >= wall_length_tolerance:
        t = Transaction(doc, 'Create Grid')
        t.Start()

        # Create the geometry line which the grid locates

        geomLine = Line.CreateBound(start, end)

        # Create a grid using the geometry line
        lineGrid = Grid.Create(doc, geomLine)
        if lineGrid is None:
            raise Exception("Create a new straight grid failed.")

        # Modify the name of the created grid
        #lineGrid.Name = "A"

        t.Commit()
        print("Created Grid Successfully")

for element_id in h_walls:
    Wall = doc.GetElement(element_id)
    # print('Wall ID - {}'.format(element_id))

    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)
    # print('Wall End Pt 0 (for Wall ID - {}): {}'.format(element_id, wep0))
    # print('Wall End Pt 1 (for Wall ID - {}): {}'.format(element_id, wep1))
    print('*' * 100)

    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep1[0], wep1[1], 0)

    wall_length = start.DistanceTo(end)

    # print(start)
    # print(end)
    if wall_length >= wall_length_tolerance:
        t = Transaction(doc, 'Create Grid')
        t.Start()

        # Create the geometry line which the grid locates

        geomLine = Line.CreateBound(start, end)

        # Create a grid using the geometry line
        lineGrid = Grid.Create(doc, geomLine)
        if lineGrid is None:
            raise Exception("Create a new straight grid failed.")

        # Modify the name of the created grid
        # lineGrid.Name = "A"

        t.Commit()
        print("Created Grid Successfully")



