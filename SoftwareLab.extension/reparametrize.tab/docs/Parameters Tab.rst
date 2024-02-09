Parameters Tab
=================

This tab involves creation of Global Parameters which will contain the distance between the created grid and existing building element.

Usage
-----

**Note: The following steps shall be proceeded after executing the steps from Grids Tab**

1. Click the ``Create Parameter`` button.
2. This button creates global parameter whose values are the distance between building element and grid and associates the parameter with the building element
3. Click the ``Create Wall-Parameter Dictionary`` button.
4. This button will create .json file which will consist of Dictionary B, where key shall be Wall Element ID and value shall be Global Parameter ID.

Create Parameter
-----------------
The following is the python script for ``Create Parameter`` button

.. code-block:: python

    # -*- coding: utf-8 -*-

    # Name of the button displayed in Revit API
    __title__ = "Create Parameter"
    # Description of the tool
    __doc__ = """This is a tool to create global parameter whose values are the distance between building element and grid."""

    # IMPORTS
    # ==================================================
    import json
    import clr

    # Additional imports related to Revit
    from Autodesk.Revit.DB import *
    from pyrevit import revit, forms

    #VARIABLES
    # ==================================================
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    app = __revit__.Application
    rvt_year = int(app.VersionNumber)

    # CLASSES & FUNCTIONS
    # ==================================================
    def feet_to_mm(feet):
        """Convert feet to millimeters."""
        inches = feet * 12
        mm = inches * 25.4
        return mm

    def calculate_distance(point1, point2):
        """Calculate the distance between two points."""
        distance = abs(point2 - point1)
        return distance

    def find_minimum_value(values):
        """Find the minimum value in a list."""
        min_value = float('inf')  # Initialize with a large value

        for value in values:
            if value < min_value:
                min_value = value

        return min_value

    def extract_element_ids(element_ids):
        """Extract element IDs from a list."""
        element_ids_str = str(element_ids)
        extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)
        element_ids_int = [int(id_str) for id_str in extracted_ids]
        return element_ids_int

    def extract_element_ids_from_dict(input_dict):
        """Extract element IDs from a dictionary."""
        extracted_dict = {}

        for key, value in input_dict.items():
            extracted_key = int(re.search(r'\d+', str(key)).group()) if re.search(r'\d+', str(key)) else None
            extracted_value = int(re.search(r'\d+', str(value)).group()) if re.search(r'\d+', str(value)) else None

            if extracted_key is not None and extracted_value is not None:
                extracted_dict[extracted_key] = extracted_value

        return extracted_dict

    def create_new_global_parameter(document, name, value):
        """Create a new global parameter in Revit."""
        if not GlobalParametersManager.AreGlobalParametersAllowed(document):
            raise System.InvalidOperationException("Global parameters are not permitted in the given document")
        if not GlobalParametersManager.IsUniqueName(document, name):
            raise System.ArgumentException("Global parameter with such name already exists in the document", "name")
        
        # Initialize the global parameter ID
        gpid = ElementId.InvalidElementId
        
        # Start a transaction for creating the global parameter
        with Transaction(document, "Create Global Parameter") as trans:
            trans.Start()
            
            # Create a global parameter with the given name and type Length
            gp = GlobalParameter.Create(document, name, SpecTypeId.Length)
            
            # Check if the global parameter was created successfully
            if gp is not None:
                # Set the value for the global parameter
                gp.SetValue(DoubleParameterValue(value))
                gpid = gp.Id
            
            # Commit the transaction
            trans.Commit()
        
        return gpid

    def mm_to_feet(mm):
        """Convert millimeters to feet."""
        feet = mm * 0.00328084
        return feet

    # MAIN
    # ==================================================

    # Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
    file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

    # Open the JSON file and load its contents into a dictionary
    with open(file_path_dictA, 'r') as file:
        dictA = json.load(file)

    # Initialize lists to store wall element IDs and corresponding distances
    wall_element_ids = []
    min_distances = []

    # Loop through the items in dictionary A
    for key, value in dictA.items():
        print("Key: {}, Value: {}".format(key, value))

        # Get wall and grid elements based on their IDs
        wall = doc.GetElement(ElementId(int(key)))
        grid = doc.GetElement(ElementId(int(value)))

        # Get wall coordinates and orientation
        Wall_x = wall.Location.Curve.Origin.X
        Wall_y = wall.Location.Curve.Origin.Y
        Wall_orientation = abs(wall.Location.Curve.Direction.Y)

        # Get coordinates of grid (which are parallel to wall)
        Grid_x = grid.Curve.Origin.X
        Grid_y = grid.Curve.Origin.Y

        # Calculate distance between wall and grid based on orientation
        if Wall_orientation == 1:  # Horizontal wall
            Wall_mm_value = feet_to_mm(Wall_x)
            Grid_mm_value = feet_to_mm(Grid_x)
        else:  # Vertical wall
            Wall_mm_value = feet_to_mm(Wall_y)
            Grid_mm_value = feet_to_mm(Grid_y)

        # Calculate distance and print the result
        distance = calculate_distance(Wall_mm_value, Grid_mm_value)
        print('Distance between Wall {} and Grid {}: {}'.format(int(key), int(value), distance))

        # Append wall element ID and corresponding distance to lists
        wall_element_ids.append(int(key))
        min_distances.append(distance)

    # Create a dictionary to store wall element IDs and their corresponding minimum distances
    min_distance_dict = {element_id: min_distance for element_id, min_distance in zip(wall_element_ids, min_distances)}
    print(min_distance_dict)

    # Loop through the items in min_distance_dict and create global parameters
    for x, y in min_distance_dict.items():
        parameter_name = 'Wall-Grid_Distance_(Wall_EID_{})'.format(x)
        parameter_value = mm_to_feet(y)

        # Call the function to create the new global parameter
        global_parameter_id = create_new_global_parameter(doc, parameter_name, parameter_value)

        # Print the ID of the created global parameter
        print("Created Global Parameter ID:", global_parameter_id)

    # Extract the existing global parameter IDs
    parameter_id = []
    all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)

    # Loop through the global parameters and print their IDs
    for p_id in all_global_parameter_ids:
        p = doc.GetElement(p_id)
        print('GP Name: {}; ID: {}'.format(p.Name, p_id))
        parameter_id.append(p_id)

    # Extract numeric values from the global parameter IDs
    parameter_id_int = extract_element_ids(parameter_id)
    print(parameter_id_int)

    # Extract wall element IDs from dictionary A
    wall_element_ids = list(dictA.keys())
    print("wall_element_ids", wall_element_ids)


Create Wall-Parameter Dictionary
--------------------------------
The following is the python script for ``Create Wall-Parameter Dictionary`` button

.. code-block:: python

    # -*- coding: utf-8 -*-
    __title__ = "Create Wall-Parameter Dictionary"
    __doc__ = """This is a tool to create Wall-Parameter Dictionary"""

    # IMPORTS
    # ==================================================
    import json
    import clr

    # Additional imports related to Revit
    from Autodesk.Revit.DB import *
    from pyrevit import revit, forms

    #VARIABLES
    # ==================================================
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    app = __revit__.Application
    rvt_year = int(app.VersionNumber)

    # CLASSES & FUNCTIONS
    # ==================================================
    def feet_to_mm(feet):
        """Convert feet to millimeters."""
        inches = feet * 12
        mm = inches * 25.4
        return mm

    def calculate_distance(point1, point2):
        """Calculate the distance between two points."""
        distance = abs(point2 - point1)
        return distance

    def find_minimum_value(values):
        """Find the minimum value in a list."""
        min_value = float('inf')  # Initialize with a large value

        for value in values:
            if value < min_value:
                min_value = value

        return min_value

    def extract_element_ids(element_ids):
        """Extract element IDs from a list."""
        element_ids_str = str(element_ids)
        extracted_ids = re.findall(r'\[([0-9]+)\]', element_ids_str)
        element_ids_int = [int(id_str) for id_str in extracted_ids]
        return element_ids_int

    # MAIN
    # ==================================================

    # Specify the path to JSON file containing dictionary A {wall1: grid1, wall2: grid2, wall3: grid2, wall4: grid3}
    file_path_dictA = r'C:\Users\harsh\OneDrive\Documents\newew\dictA.json'

    # Open the JSON file and load its contents into a dictionary
    with open(file_path_dictA, 'r') as file:
        dictA = json.load(file)

    print(dictA)
    print("Type dictA: ", type(dictA))

    # Extract existing global parameter IDs
    parameter_id = []
    all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)

    # Loop through global parameters and collect their IDs
    for p_id in all_global_parameter_ids:
        p = doc.GetElement(p_id)
        parameter_id.append(p_id)

    # Extract numeric values from the global parameter IDs
    parameter_id_int = extract_element_ids(parameter_id)
    print(parameter_id_int)

    # Extract wall element IDs from dictionary A
    wall_element_ids = list(dictA.keys())
    print("wall_element_ids", wall_element_ids)

    # Initialize an empty dictionary to store the mapping between walls and parameters
    dictB = {}

    # Iterate through wall element IDs and corresponding parameter IDs
    for k, v in zip(wall_element_ids, parameter_id_int):
        dictB[k] = v

    # Convert both keys and values to strings in the dictionary
    dictB_str = {str(key): str(value) for key, value in dictB.items()}

    # Specify the file path for the output JSON file
    file_path_dictB = r'C:\Users\harsh\OneDrive\Documents\newew\dictB.json'

    # Write the dictionary to a JSON file
    with open(file_path_dictB, 'w') as fp:
        json.dump(dictB_str, fp, indent=4)

    print("JSON file created successfully.")
