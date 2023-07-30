# -*- coding: utf-8 -*-

#Practicing FilteredElementCollector

__title__ = "Wall Filter"  # Name of button displayed in Revit API
__doc__ = """This is a simple tool to filter wall"""
# """
# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
# """
from Autodesk.Revit.DB import *

# pyRevit
from pyrevit import forms

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

all_walls = FilteredElementCollector(doc).OfClass(Wall).WhereElementIsNotElementType().ToElements()
print(all_walls)

# Next Step - need to extract all the grids - Important