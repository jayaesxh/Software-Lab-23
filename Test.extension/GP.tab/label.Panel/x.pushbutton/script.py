# -*- coding: utf-8 -*-
__title__ = "Assign Dimensions to Walls"
__author__ = "Jayesh"
__version__ = "Version 1.0"
__doc__ = """ Description:  """

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# ====================================================================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Reference, ReferenceArray, Line

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

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ====================================================================================================
with Transaction(doc, "Create Dimension") as t:
    t.Start()

    # Get All Walls
    all_walls = FilteredElementCollector(doc).OfClass(Wall).WhereElementIsNotElementType().ToElements()

    for wall in all_walls:
        wall_curve = wall.Location.Curve

        # CREATE REFERENCE ARRAY
        refArray = ReferenceArray()

        refArray.Append(Reference(wall))

        # CREATE REFERENCE LINE FOR DIMENSION
        start = wall_curve.GetEndPoint(0)
        end = wall_curve.GetEndPoint(1)
        line = Line.CreateBound(start, end)

    # CREATE NEW DIMENSION
    doc.Create.NewDimension(active_view, line, refArray)

    t.Commit()
