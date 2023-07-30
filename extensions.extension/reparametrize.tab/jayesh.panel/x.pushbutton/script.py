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

# Get wall
wall_id = ElementId(402604)
Wall = doc.GetElement(wall_id)
wep0 = Wall.Location.Curve.GetEndPoint(0)
wep1 = Wall.Location.Curve.GetEndPoint(1)
print('Wall End Pt 0 (for Wall ID - {}): {}'.format(wall_id, wep0))
print('Wall End Pt 1 (for Wall ID - {}): {}'.format(wall_id, wep1))
print('*' * 50)


grid_id = ElementId(605814)
Grid = doc.GetElement(grid_id)
gep0 = Grid.Curve.GetEndPoint(0)
gep1 = Grid.Curve.GetEndPoint(1)
print('Grid End Pt 0 (for Grid ID - {}): {}'.format(grid_id, gep0))
print('Grid End Pt 1 (for Grid ID - {}): {}'.format(grid_id, gep1))

print('*' * 50)

print(gep1[0])
print(gep1[1])
print(gep1[1]-5)
print(gep1[2])



start = XYZ(wep0[0], wep0[1]-5, 0)
end = XYZ(gep1[0], wep0[1]-5, 0)

t = Transaction(doc, 'Create Dimension')
t.Start()



lines = Line.CreateBound(start, end)

# CREATE REFERENCE ARRAY
refArray = ReferenceArray()
refArray.Append(Reference(Wall))
refArray.Append(Reference(Grid))

# create_dimension = create_dim(doc,lines)

# CREATE NEW DIMENSION
doc.Create.NewDimension(active_view, lines, refArray)
t.Commit()
print("Created Dimension Successfully")















