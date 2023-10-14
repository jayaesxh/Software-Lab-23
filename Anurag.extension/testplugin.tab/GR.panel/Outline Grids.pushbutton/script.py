# -*- coding: utf-8 -*-
__title__ = "Outmost Grids"
__doc__ = """This script is part of YouTube video
where I explain RevitAPI Parameters and how to work with them.

You can support my channel on:
www.patreon.com/ErikFrits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
# ==================================================
# Regular + Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Line, Grid, XYZ, ElementTransformUtils, BoundingBoxXYZ, BoundingBoxIntersectsFilter
from pyrevit import revit, DB
import clr
# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================

uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc     =__revit__.ActiveUIDocument.Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

# Getting all walls and grids
all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()
all_grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()

 # Initialize lists to store wall and grid positions
wall_positions = []
grid_positions = []

# Retrieve wall elements
# wall_collector = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_Walls)
wall_collector = FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_Walls)
wall_elements = wall_collector.ToElements()

# Retrieve grid elements
grid_collector = FilteredElementCollector(revit.doc).OfClass(Grid)
grid_elements = grid_collector.ToElements()

# # Loop through wall elements and store their locations
# for wall in wall_elements:
#     location_curve = wall.Location
#     if location_curve:
#         start_point = location_curve.GetEndPoint(0)
#         end_point = location_curve.GetEndPoint(1)
#         wall_positions.extend([start_point, end_point])

# Loop through grid elements and store their locations
for grid in grid_elements:
    grid_line = grid.Curve
    if grid_line:
        start_point = grid_line.GetEndPoint(0)
        end_point = grid_line.GetEndPoint(1)
        grid_positions.extend([start_point, end_point])

# Now store the positions of walls and grids in the lists
# print("Wall Positions:")
# for position in wall_positions:
#     print(position)

print("Grid Positions:")
for position in grid_positions:
    print(position)


#
# for element_id in all_walls:
#     Wall = doc.GetElement(element_id)
#     Wall_x = Wall.Location.Curve.Origin.X
#     print('Wall_p1 for Element ID- {}: {}'.format(element_id, Wall_x))
#     Wall_y = Wall.Location.Curve.Origin.Y
#     print('Wall_p2 for Element ID- {}: {}'.format(element_id, Wall_y))
#
#     print(wall_positions.append([Wall_x, Wall_y]))

# for element_id in all_grids:
#     Grid = doc.GetElement(element_id)
#     Grid_x = Grid.Curve.Origin.X
#     print('Grid_p1 for Element ID- {}: {}'.format(element_id, Grid_x))
#     Grid_y = Grid.Curve.Origin.Y
#     print('Grid_p2 for Element ID- {}: {}'.format(element_id, Grid_y))
#
#     print(grid_positions.extend([Grid_x, Grid_y]))

# Getting min and max coordinates for grids

def minimum_value(values):
    min_value = float('inf')

    for value in values:
        if value < min_value:
            min_value = value

    return min_value



def max_value(values):
    max_value = float('inf')


    for value in values:
        if value > max_value:
            max_value = value

    return max_value



threshold = 0.00001
x_min = minimum_value(grid_positions)
x_max = max_value(grid_positions)
y_min = minimum_value(grid_positions)
y_max = max_value(grid_positions)

print('least_coordinate - {},{}'.format(x_min, y_min))
print('max_coordinate - {},{}'.format(x_max, y_max))

def get_extreme_most_grids():
    # Retrieve all grid elements
    # grid_collector = DB.FilteredElementCollector(revit.doc).OfCategory(DB.BuiltInCategory.OST_Grids)
    # grid_elements = grid_collector.ToElements()
    # grid_collector = FilteredElementCollector(revit.doc).OfCategory(BuiltInCategory.OST_Grids)
    # grid_elements = grid_collector.ToElements()
    grid_collector = FilteredElementCollector(revit.doc).OfClass(Grid)
    grid_elements = grid_collector.ToElements()

   
    # Initialize variables to store extreme coordinates
    min_x = float('inf')  # Initialize with positive infinity
    max_x = float('-inf')  # Initialize with negative infinity
    min_y = float('inf')
    max_y = float('-inf')

    i = 0
    # Iterate through grid elements and update extreme coordinates
    for grid in grid_elements:
        # Get the endpoints of the grid line
        start_point = grid.Curve.GetEndPoint(0)
        end_point = grid.Curve.GetEndPoint(1)

        # Update the extreme coordinates
        min_x = min(min_x, start_point.X, end_point.X)
        max_x = max(max_x, start_point.X, end_point.X)
        min_y = min(min_y, start_point.Y, end_point.Y)
        max_y = max(max_y, start_point.Y, end_point.Y)

        # Print the extreme coordinates
        print(str(i) + " " + "Extreme Most Grid Coordinates:")
        print("Minimum X:", min_x)
        print("Maximum X:", max_x)
        print("Minimum Y:", min_y)
        print("Maximum Y:", max_y)
        i += 1

# Call the function to get the extreme most grids' coordinates
get_extreme_most_grids()