# -*- coding: utf-8 -*-
#Practicing FilteredElementCollector

__title__ = "Grid Filter"  # Name of button displayed in Revit API
__doc__ = """This is a simple tool to filter grids"""
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

all_grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()
print(all_grids)

# Next Step - need to extract all the grids - Important