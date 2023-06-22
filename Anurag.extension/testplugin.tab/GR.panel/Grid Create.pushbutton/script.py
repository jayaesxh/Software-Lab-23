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

def create_grids(document, lines):
    transaction = Transaction(document, "Create Grids")
    transaction.Start()

    try:
        created_grids = []

        for line in lines:
            grid = Grid.Create(document, line)
            print("Grid created successfully.")
            print("Grid Id:", grid.Id)
            print("Grid Name:", grid.Name)

            created_grids.append(grid)


        transaction.Commit()
        print("Transaction committed successfully")
        return grid
    except Exception as e:
        transaction.Rollback()
        print("Transaction failed. Rolled Back")
        print("Error:", str(e))




lines  = [Line.CreateBound(XYZ(0,-95.871,0), XYZ(10,0,0))]
create_grid = create_grids(doc, lines)




