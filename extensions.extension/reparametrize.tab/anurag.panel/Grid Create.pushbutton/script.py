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

def get_wall_elements(document):
    wall_collector = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Walls)
    wall_elements = list(wall_collector)
    return wall_elements


def create_grids_from_wall(document, wall, grid_length):
    # Start a transaction
    transaction = Transaction(document, "Create Grids from Wall")
    transaction.Start()

    try:
        created_grids = []

        # Get the bounding box of the wall
        bounding_box = wall.get_BoundingBox(None)

        # Check if the bounding box is valid
        if bounding_box:
            min_point = bounding_box.Min
            max_point = bounding_box.Max

            # Calculate the desired end point for the grids based on the grid length
            grid_end_point = XYZ(min_point.X + grid_length, min_point.Y, min_point.Z)

            # Create the grid lines based on the bounding box points and the desired end point
            horizontal_line = Line.CreateBound(XYZ(min_point.X, min_point.Y, min_point.Z), grid_end_point)
            vertical_line = Line.CreateBound(XYZ(max_point.X, min_point.Y, min_point.Z),
                                             XYZ(max_point.X, max_point.Y, max_point.Z))

            # Get the wall's orientation
            wall_direction = wall.Orientation

            # Rotate the grid lines to align with the wall's orientation
            horizontal_line = Line.CreateBound(horizontal_line.GetEndPoint(0),
                                               horizontal_line.GetEndPoint(0) + wall_direction)
            vertical_line = Line.CreateBound(vertical_line.GetEndPoint(0),
                                             vertical_line.GetEndPoint(0) + wall_direction)

            # Creating horizontal grid
            horizontal_grid = Grid.Create(document, horizontal_line)
            created_grids.append(horizontal_grid)

            # Creating vertical grid
            vertical_grid = Grid.Create(document, vertical_line)
            created_grids.append(vertical_grid)

        # Commit the transaction
        transaction.Commit()
        print("Transaction committed successfully.")

        return created_grids
    except Exception as e:
        # Rollback the transaction in case of an error
        transaction.RollBack()
        print("Transaction failed. Rolled back.")
        print("Error:", str(e))


# Active Revit document
active_doc = __revit__.ActiveUIDocument.Document

wall_elements = get_wall_elements(active_doc)

# Set the desired grid length
grid_length = 10.0

# Create grids for each wall element
for wall in wall_elements:
    created_grids = create_grids_from_wall(active_doc, wall, grid_length)




