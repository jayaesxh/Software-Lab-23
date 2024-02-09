Getting Started
===============

Model Re-Parametrizing is a Revit extension written in Python that can help you 
to automate parameter creation in order to make models flexible to explore alternate design possibilities.


Installation
------------

To install this extension, 
download the extension `zip <https://github.com/jayaesxh/Software-Lab-23>`_
. Open the *pyRevit* tab, 
click on *pyRevit* > *Extensions* to open the extensions manager and 
follow `these <https://www.notion.so/Install-Extensions-0753ab78c0ce46149f962acc50892491>`_ instructions.

Create Wall-Grids
-----------------

*Objective:*

*Script Anatomy*

1. Filtered Element Collectors:
The script uses FilteredElementCollector to retrieve all walls, grids, and structural columns in the Revit model.

2. Wall Orientation:
Walls are categorized into vertical (v_walls) and horizontal (h_walls) based on their orientation.

3. Create Grids for Vertical Walls:
For each vertical wall, the script checks its length and creates a grid if the length exceeds a specified tolerance.

4. Create Grids for Horizontal Walls:
Similar to vertical walls, the script checks the length of each horizontal wall and creates a grid if the length is above the tolerance.

5. Transaction Management:
Transactions (t) are used to manage the creation of grids, ensuring that changes are committed to the Revit model.

6. Grid Creation:
The script creates grids using the Grid.Create method based on the start and end points of the walls.

.. image:: images/Bild1.png
 :width: 600

The following is the python script for ``Create Wall-Grids`` button
