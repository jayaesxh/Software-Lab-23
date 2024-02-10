Dimensions Tab
=================

This tab involves creation of labelled dimensions between building elements and grids.

Usage
-----

**Note: The following steps shall be proceeded after executing the steps from Parameters Tab**

1. Click the ``Create/Label Dimension`` button.
2. This button creates labelled dimension between building elements and grids. By clicking on the label of dimension, the user can control the distance of building element from the grid.
3. Click the ``Create Dimensions based on Outer Grids`` button.
4. This button creates labelled dimension between building elements and outer grids. By clicking on the label of dimension, the user can control the distance of building element from the outer grid.

*Objective:* This script creates and labels dimensions in Revit based on predefined dictionaries (dictA, dictB) and associates them with global parameters.

 

*Script Anatomy:*

1. Functions Section:

``feet_to_mm (feet)``: Converts feet to millimeters.

``create_new_dimension_along_line (document, line)``: Creates a new dimension along a given line.

``extract_element_ids (element_ids)``: Extracts element IDs from a list.

 

2. Dictionary Loading:

It loads two dictionaries from JSON files - ``dictA`` (mapping walls to grids) and ``dictB`` (mapping walls to global parameters).

 

3. Grid Sorting:

The script separates vertical and horizontal grids based on their orientations.

 

4. Dictionary A Separation:

It further separates ``dictA`` into dictionaries for horizontal and vertical walls/grids (``dictA_hor_dim`` and ``dictA_ver_dim``).

 

5. Horizontal Dimensions Creation:

The script creates horizontal dimensions between walls and grids, storing the resulting dimension IDs in ``dictC_hor_dim``.

 

6. Mapping to Global Parameters:

It maps global parameters from ``dictB`` to horizontal dimensions, storing the associations in ``dictD_hor_dim``.

 

7. Labeling Horizontal Dimensions:

The script labels horizontal dimensions with corresponding global parameters.

 

8. Vertical Dimensions Creation:

Similarly, vertical dimensions are created, mapped to global parameters, and labeled.

Create/Label Dimension
----------------------
The following is the python script for ``Create/Label Dimension`` button

.. code-block:: python

    # -*- coding: utf-8 -*-

    # Name of the button displayed in Revit API
    __title__ = "Create/Label Dimension"
    # Description of the tool
    __doc__ = """This is a tool to Create/Label Dimension"""

    # IMPORTS
    # ==================================================================
    import json
    import re
    from Autodesk.Revit.DB import *
    from pyrevit import revit, DB

    # .NET IMPORTS
    import clr

    clr.AddReference('System')
    from System.Collections.Generic import List

    # VARIABLES
    # =================================================================
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    app = __revit__.Application

    active_view = doc.ActiveView
    active_level = doc.ActiveView.GenLevel

    # FUNCTIONS
    # ================================================================
    def feet_to_mm(feet):
        """Convert feet to millimeters."""
        # 1 foot = 304.8 millimeters
        mm = feet * 304.8
        return mm

    def create_new_dimension_along_line(document, line):
        """Create a new dimension along a given line."""
        # Use the Start and End points of our line as the references
        references = [line.GetEndPointReference(0), line.GetEndPointReference(1)]
        
        # Create the new dimension
        dimension = document.Create.NewDimension(document.ActiveView, line, references)
        return dimension

    def extract_element_ids(element_ids):
        """Extract element IDs from a list."""
        element_ids_str = str(element_ids)
        extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)
        element_ids_int = [int(id_str) for id_str in extracted_ids]
        return element_ids_int

    # MAIN
    # =================================================================
    # Load Dictionary A from JSON file
    file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'
    with open(file_path_dictA, 'r') as file:
        dictA = json.load(file)

    # Load Dictionary B from JSON file
    file_path_dictB = r'C:\Users\harsh\OneDrive\Documents\newew\dictB.json'
    with open(file_path_dictB, 'r') as file:
        dictB = json.load(file)

    tol = app.ShortCurveTolerance

    # GRID SORTING
    v_grids = []
    h_grids = []

    # Separate vertical and horizontal grids
    for wall_id, grid_id in dictA.items():
        grid = doc.GetElement(ElementId(int(grid_id)))
        Grid_orientation = grid.Curve.Direction.Y
        if Grid_orientation == -1:
            v_grids.append(grid_id)
        elif Grid_orientation != -1:
            h_grids.append(grid_id)

    # Separate dictionary A for horizontal and vertical walls/grids
    dictA_hor_dim = {}
    dictA_ver_dim = {}

    for wall_id, grid_id in dictA.items():
        wall = doc.GetElement(ElementId(int(wall_id)))
        grid = doc.GetElement(ElementId(int(grid_id)))

        # Check if the orientations match
        if wall.Location.Curve.Direction.Y == -1 or wall.Location.Curve.Direction.Y == 1 \
                and grid.Curve.Direction.Y == -1 or grid.Curve.Direction.Y == 1:
            # For vertical grids
            dictA_hor_dim[wall_id] = grid_id
        elif wall.Location.Curve.Direction.Y != -1 or wall.Location.Curve.Direction.Y != 1 \
                and grid.Curve.Direction.Y != -1 or grid.Curve.Direction.Y != 1:
            # For horizontal grids
            dictA_ver_dim[wall_id] = grid_id

    # Create and label horizontal dimensions
    dictC_hor_dim = {}
    dictD_hor_dim = {}

    for wall_id, grid_id in dictA_hor_dim.items():
        wall = doc.GetElement(ElementId(int(wall_id)))
        grid = doc.GetElement(ElementId(int(grid_id)))

        # Create dimensions between Wall and Grid
        start = XYZ(wall.Location.Curve.GetEndPoint(0)[0], wall.Location.Curve.GetEndPoint(0)[1] - 5, 0)
        end = XYZ(grid.Curve.GetEndPoint(1)[0] + 2 * tol, wall.Location.Curve.GetEndPoint(0)[1] - 5, 0)

        # Calculate the difference between start and end
        difference = (end - start).GetLength()

        # Create and store horizontal dimensions
        t = Transaction(doc, 'Create Dimension')
        t.Start()
        lines = Line.CreateBound(start, end)
        refArray = ReferenceArray()
        refArray.Append(Reference(wall))
        refArray.Append(Reference(grid))
        dim = doc.Create.NewDimension(active_view, lines, refArray)
        t.Commit()
        dim_id = dim.Id.IntegerValue
        dictC_hor_dim[wall_id] = dim_id

    # Map global parameters to horizontal dimensions
    for wall_id_B, gp_id in dictB.items():
        for wall_id_C, dim_id_wall in dictC_hor_dim.items():
            if wall_id_B == wall_id_C:
                dictD_hor_dim[gp_id] = dim_id_wall

    # Label horizontal dimensions
    for gp_id, dim_id in dictD_hor_dim.items():
        t = Transaction(doc, 'Label Dimension')
        t.Start()
        gp = doc.GetElement(ElementId(int(gp_id)))
        label = gp.LabelDimension(ElementId(int(dim_id)))
        t.Commit()

    # Create and label vertical dimensions
    dictC_ver_dim = {}
    dictD_ver_dim = {}

    for wall_id, grid_id in dictA_ver_dim.items():
        wall = doc.GetElement(ElementId(int(wall_id)))
        grid = doc.GetElement(ElementId(int(grid_id)))

        # Create dimensions between Wall and Grid
        start = XYZ(wall.Location.Curve.GetEndPoint(0)[0] - 5, wall.Location.Curve.GetEndPoint(0)[1], 0)
        end = XYZ(wall.Location.Curve.GetEndPoint(0)[0], grid.Curve.GetEndPoint(0)[1] + 2 * tol, 0)

        # Calculate the difference between start and end
        difference = (end - start).GetLength()

        # Create and store vertical dimensions
        t = Transaction(doc, 'Create Dimension')
        t.Start()
        lines = Line.CreateBound(start, end)
        refArray = ReferenceArray()
        refArray.Append(Reference(wall))
        refArray.Append(Reference(grid))
        dim = doc.Create.NewDimension(active_view, lines, refArray)
        t.Commit()
        dim_id = dim.Id.IntegerValue
        dictC_ver_dim[wall_id] = dim_id

    # Map global parameters to vertical dimensions
    for wall_id_B, gp_id in dictB.items():
        for wall_id_C, dim_id_wall in dictC_ver_dim.items():
            if wall_id_B == wall_id_C:
                dictD_ver_dim[gp_id] = dim_id_wall

    # Label vertical dimensions
    for gp_id, dim_id in dictD_ver_dim.items():
        t = Transaction(doc, 'Label Dimension')
        t.Start()
        gp = doc.GetElement(ElementId(int(gp_id)))
        label = gp.LabelDimension(ElementId(int(dim_id)))
        t.Commit()

Create Dimensions based on Outer Grids
--------------------------------------

*Objective:* The script automates the creation of dimensions between walls and outer grids in Revit, subsequently associating these dimensions with global parameters.

 

*Script Anatomy:*


1. Filtered Element Collectors:

The script uses filtered element collectors to gather information about walls and grids in the Revit document.

 

2. Grid Sorting:

It sorts grids into vertical and horizontal based on their orientations.

 

3. Outer Grid Identification:

The script identifies the left, right, upper, and lower outer grids by finding the minimum and maximum coordinates.

 

4. Wall Sorting:

It sorts walls into vertical and horizontal based on their orientations.

 

5. Dimension Creation - Vertical Walls to Left Grid:

The script creates dimensions between vertical walls and the left outer grid.

 

6. Dimension Creation - Horizontal Walls to Lower Grid:

Similarly, dimensions are created between horizontal walls and the lower outer grid.

 

7. Global Parameter Mapping:

It maps the dimensions to global parameters and labels them accordingly.


The following is the python script for ``Create Dimensions based on Outer Grids`` button

.. code-block:: python

    # -*- coding: utf-8 -*-
    __title__ = "Create Dimensions based on Outer Grids"
    __doc__ = """This is a tool to create Dimensions based on Outer Grids"""

    # IMPORTS
    # ==================================================
    import json
    import re
    from System.Collections.Generic import List

    from Autodesk.Revit.DB import *
    from Autodesk.Revit.UI import TaskDialog

    # pyRevit
    from Autodesk.Revit.DB import GlobalParametersManager, Transaction, GlobalParameter, DoubleParameterValue, SpecTypeId

    # FUNCTIONS
    # ==================================================
    def mm_to_feet(mm_value):
        # Convert millimeters to feet
        return mm_value * 0.00328084

    def feet_to_mm(feet_value):
        # Convert feet to millimeters
        return feet_value * 304.8

    def find_minimum_value(values):
        # Find the minimum value in a list
        return min(values, default=float('inf'))

    def find_maximum_value(values):
        # Find the maximum value in a list
        return max(values, default=float('-inf'))

    def extract_element_ids(element_ids):
        # Extract element IDs from ElementId objects
        element_ids_str = str(element_ids)
        extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)
        return [int(id_str) for id_str in extracted_ids]

    def drive_selected_dimensions(document, name, value, dimset):
        # Drive selected dimensions using a global parameter
        if not GlobalParametersManager.AreGlobalParametersAllowed(document):
            raise ValueError("Global parameters are not permitted in the given document")

        if not GlobalParametersManager.IsUniqueName(document, name):
            raise ValueError("Global parameter with such name already exists in the document")

        if value <= 0.0:
            raise ValueError("Value of a global parameter that drives dimension must be a positive number")

        n_labeled_dims = 0

        with Transaction(document, "Create Global Parameter") as trans:
            trans.Start()
            newgp = GlobalParameter.Create(document, name, SpecTypeId.Length)
            
            if newgp is not None:
                newgp.SetValue(DoubleParameterValue(value))
                
                for elemid in dimset:
                    elemid_ = (doc.GetElement(ElementId(elemid))).Id
                    if newgp.CanLabelDimension(elemid_):
                        newgp.LabelDimension(elemid_)
                        n_labeled_dims += 1

                trans.Commit()

    def create_new_labelled_global_parameter(document, name, value):
        # Create a new labeled global parameter
        if not GlobalParametersManager.AreGlobalParametersAllowed(document):
            raise System.InvalidOperationException("Global parameters are not permitted in the given document")
        
        if not GlobalParametersManager.IsUniqueName(document, name):
            raise System.ArgumentException("Global parameter with such name already exists in the document", "name")
        
        gpid = ElementId.InvalidElementId
        
        with Transaction(document, "Create Global Parameter") as trans:
            trans.Start()
            gp = GlobalParameter.Create(document, name, SpecTypeId.Length)
            if gp is not None:
                gp.SetValue(DoubleParameterValue(value))
                gpid = gp.Id
            trans.Commit()
        
        return gpid

    # VARIABLES
    # ==================================================
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    app = __revit__.Application
    active_view = doc.ActiveView
    active_level = doc.ActiveView.GenLevel

    # MAIN
    # ==================================================

    # Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
    file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

    # Open the JSON file and load its contents into a dictionary
    with open(file_path_dictA, 'r') as file:
        dictA = json.load(file)

    print(dictA)
    print("Type dictA: ", type(dictA))

    # GET ALL WALLS
    all_walls = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElementIds()

    # GET ALL GRIDS
    all_grids = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElementIds()

    # GRID SORTING
    v_grids = []
    h_grids = []

    for element_id in all_grids:
        Grid = doc.GetElement(element_id)

        Grid_orientation = Grid.Curve.Direction.Y
        if Grid_orientation == 1 or Grid_orientation == -1:
            v_grids.append(element_id)
        elif Grid_orientation != 1 and Grid_orientation != -1:
            h_grids.append(element_id)

    # Get outline grids
    x_coordinates = []
    y_coordinates = []

    # Get xmin, xmax
    for element_ids in v_grids:
        Grid = doc.GetElement(element_ids)
        Grid_x = Grid.Curve.Origin.X
        x_coordinates.append(Grid_x)

    xmin = find_minimum_value(x_coordinates)
    xmax = find_maximum_value(x_coordinates)

    for element_ids in h_grids:
        Grid = doc.GetElement(element_ids)
        Grid_y = Grid.Curve.Origin.Y
        y_coordinates.append(Grid_y)

    ymin = find_minimum_value(y_coordinates)
    ymax = find_maximum_value(y_coordinates)

    # Get corresponding grid to min/max coordinates
    grid_id_xmin = v_grids[x_coordinates.index(xmin)]
    grid_id_xmax = v_grids[x_coordinates.index(xmax)]
    grid_id_ymin = h_grids[y_coordinates.index(ymin)]
    grid_id_ymax = h_grids[y_coordinates.index(ymax)]

    outline_grids = [grid_id_xmin, grid_id_xmax, grid_id_ymin, grid_id_ymax]
    outline_grids_int = extract_element_ids(outline_grids)
    print(outline_grids_int)

    left_grid = outline_grids_int[0]
    right_grid = outline_grids_int[1]
    up_grid = outline_grids_int[3]
    down_grid = outline_grids_int[2]

    # WALL SORTING
    v_walls = []
    h_walls = []
    for wall_id, grid_id in dictA.items():
        wall = doc.GetElement(ElementId(int(wall_id)))
        wall_orientation = wall.Location.Curve.Direction.Y
        
        if wall_orientation == 1 or wall_orientation == -1:
            v_walls.append(wall_id)
        elif wall_orientation != 1 or wall_orientation != -1:
            h_walls.append(wall_id)

    print(v_walls)
    print("Vertical Wall IDs: {}".format(';'.join(v_walls)))
    print(h_walls)
    print("Horizontal Wall IDs: {}".format(';'.join(h_walls)))

    tol = app.ShortCurveTolerance

    dict_LG_VW = {left_grid: v_walls}
    dict_RG_VW = {right_grid: v_walls}
    dict_UG_HW = {up_grid: h_walls}
    dict_DG_HW = {down_grid: h_walls}

    dict_VW_LD = {}
    dim_LD = []
    dict_HW_DD = {}
    dim_DD = []

    print(dict_LG_VW)

    # VERTICAL WALLS

    # VERTICAL WALLS - LEFT GRID
    for wall_id in v_walls:
        wall = doc.GetElement(ElementId(int(wall_id)))
        grid = doc.GetElement(ElementId(int(left_grid)))

        wep0 = wall.Location.Curve.GetEndPoint(0)
        wep1 = wall.Location.Curve.GetEndPoint(1)

        gep0 = grid.Curve.GetEndPoint(0)
        gep1 = grid.Curve.GetEndPoint(1)

        # Create dimensions between Wall and Grid
        start = XYZ(wep0[0], wep0[1] - 5, 0)
        end = XYZ((gep1[0] + 2 * tol), wep0[1] - 5, 0)

        t = Transaction(doc, 'Create Dimension')
        t.Start()

        lines = Line.CreateBound(start, end)

        # CREATE REFERENCE ARRAY
        refArray = ReferenceArray()
        refArray.Append(Reference(wall))
        refArray.Append(Reference(grid))

        # CREATE NEW DIMENSION
        dim = doc.Create.NewDimension(active_view, lines, refArray)
        t.Commit()

        dim_id = dim.Id.IntegerValue
        dim_LD.append(dim_id)
        dict_VW_LD[wall_id] = dim_id

    print(dict_VW_LD)
    print(dim_LD)

    for wall_id, dim_id in dict_VW_LD.items():
        gp_name = "Distance_Left_Grid_and_Wall_ID_{}".format(int(wall_id))
        dim = doc.GetElement(ElementId(int(dim_id)))
        dim_value = dim.Value
        print(feet_to_mm(dim_value))

        global_parameter_id = create_new_labelled_global_parameter(doc, gp_name, dim_value)

        # Label Dimension
        t = Transaction(doc, 'Label Dimension')
        t.Start()

        gp = doc.GetElement(global_parameter_id)
        label = gp.LabelDimension(ElementId(dim_id))

        t.Commit()
        print("Labeled Dimension Successfully")

    # HORIZONTAL WALLS

    # HORIZONTAL WALLS - LOWER GRID
    for wall_id in h_walls:
        wall = doc.GetElement(ElementId(int(wall_id)))
        grid = doc.GetElement(ElementId(int(down_grid)))

        wep0 = wall.Location.Curve.GetEndPoint(0)
        wep1 = wall.Location.Curve.GetEndPoint(1)

        gep0 = grid.Curve.GetEndPoint(0)
        gep1 = grid.Curve.GetEndPoint(1)

        # Create dimensions between Wall and Grid
        start = XYZ(wep0[0], wep0[1], 0)
        end = XYZ(wep0[0], (gep0[1] + 2 * tol), 0)

        t = Transaction(doc, 'Create Dimension')
        t.Start()

        lines = Line.CreateBound(start, end)

        # CREATE REFERENCE ARRAY
        refArray = ReferenceArray()
        refArray.Append(Reference(wall))
        refArray.Append(Reference(grid))

        # CREATE NEW DIMENSION
        dim = doc.Create.NewDimension(active_view, lines, refArray)
        t.Commit()

        dim_id = dim.Id.IntegerValue
        dim_DD.append(dim_id)
        dict_HW_DD[wall_id] = dim_id

    print(dict_HW_DD)
    print(dim_DD)

    for wall_id, dim_id in dict_HW_DD.items():
        gp_name = "Distance_Lower_Grid_and_Wall_ID_{}".format(int(wall_id))
        dim = doc.GetElement(ElementId(int(dim_id)))
        dim_value = dim.Value
        print(feet_to_mm(dim_value))

        global_parameter_id = create_new_labelled_global_parameter(doc, gp_name, dim_value)

        # Label Dimension
        t = Transaction(doc, 'Label Dimension')
        t.Start()

        gp = doc.GetElement(global_parameter_id)
        label = gp.LabelDimension(ElementId(dim_id))

        t.Commit()
        print("Labeled Dimension Successfully")
