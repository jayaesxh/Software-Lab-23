# -*- coding: utf-8 -*-
#Practicing FilteredElementCollector

__title__ = "Grid Create"  # Name of button displayed in Revit API
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
from Autodesk.Revit.DB import Line, Grid, XYZ
from Autodesk.Revit.DB import Transaction

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
# Get wall
# GET ALL WALLS
all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()

for element_id in all_walls:
    Wall = doc.GetElement(element_id)

    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)
    print('Wall End Pt 0 (for Wall ID - {}): {}'.format(element_id, wep0))
    print('Wall End Pt 1 (for Wall ID - {}): {}'.format(element_id, wep1))
    print('*' * 100)

    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep1[0], wep1[1], 0)

    print(start)
    print(end)

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



