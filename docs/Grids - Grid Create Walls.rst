Create Wall-Grids
=================

This tool creates grids based on the orientation of walls in the Revit model.

Usage
-----

1. Open the Revit model where you want to create grids.
2. Run the "Create Wall-Grids" tool.
3. The tool will identify the orientation of walls and create corresponding grids.

```python
# -*- coding: utf-8 -*-
# Practicing FilteredElementCollector

__title__ = "Create Wall-Grids"  # Name of button displayed in Revit API
__doc__ = """This is a simple tool to create grids"""

# Import necessary modules
from Autodesk.Revit.DB import *
from pyrevit import forms
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Line, Grid, XYZ, ElementTransformUtils, BoundingBoxXYZ
from Autodesk.Revit.DB import Transaction
from pyrevit import revit, DB

# Document and UI Variables
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application

# Filtered Element Collectors

# Creating grids using wall reference and setting up the particular grid length

# Get walls, grids, and columns
all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
all_grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()
all_columns = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()

# Wall Orientation

v_walls = []
h_walls = []

# Categorize walls based on orientation
for element_id in all_walls:
    Wall = doc.GetElement(element_id)
    Wall_x = Wall.Location.Curve.Origin.X
    Wall_y = Wall.Location.Curve.Origin.Y
    Wall_orientation = abs(Wall.Location.Curve.Direction.Y)

    if Wall_orientation == 1:
        v_walls.append(element_id)
    elif Wall_orientation != 1:
        h_walls.append(element_id)

# Create Grids for Vertical Walls

wall_length_tolerance = 2.5  # 2.5 feet = 0.75 meter

for element_id in v_walls:
    Wall = doc.GetElement(element_id)
    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)

    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep1[0], wep1[1], 0)

    wall_length = start.DistanceTo(end)

    if wall_length >= wall_length_tolerance:
        t = Transaction(doc, 'Create Grid')
        t.Start()

        geomLine = Line.CreateBound(start, end)
        lineGrid = Grid.Create(doc, geomLine)
        
        t.Commit()
        print("Created Grid Successfully")

# Create Grids for Horizontal Walls

for element_id in h_walls:
    Wall = doc.GetElement(element_id)
    wep0 = Wall.Location.Curve.GetEndPoint(0)
    wep1 = Wall.Location.Curve.GetEndPoint(1)

    start = XYZ(wep0[0], wep0[1], 0)
    end = XYZ(wep1[0], wep1[1], 0)

    wall_length = start.DistanceTo(end)

    if wall_length >= wall_length_tolerance:
        t = Transaction(doc, 'Create Grid')
        t.Start()

        geomLine = Line.CreateBound(start, end)
        lineGrid = Grid.Create(doc, geomLine)
        
        t.Commit()
        print("Created Grid Successfully")
