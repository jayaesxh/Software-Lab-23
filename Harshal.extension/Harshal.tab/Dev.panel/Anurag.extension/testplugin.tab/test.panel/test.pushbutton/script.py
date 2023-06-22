# -*- coding: utf-8 -*-
__title__ = "03 - RevitAPI: Parameters"
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
from xlwings.constants import ParameterType

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
# ==================================================

uidoc = __revit__.ActiveUIDocument
app = __revit__.Application


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝ MAIN
# ==================================================

def create_new_global_parameter(document, name, value):
    t = Transaction(document, 'Creating Global Parameters')
    t.Start()

    # Create a GP with the given name and type Length
    gp = GlobalParameter.Create(document, name, ParameterType.Length)
    if gp is not None:
        # If created successfully, assign it a value
        # Note: Parameters of type Length accept Double values
        gp.SetValue(DoubleParameterValue(value))
        gpid = gp.Id

    t.Commit()

    return gpid


# Example usage
doc = __revit__.ActiveUIDocument.Document
parameter_name = "MyGlobalParameter"
parameter_value = 10.0

# Call the function to create the new global parameter
global_parameter_id = create_new_global_parameter(doc, parameter_name, parameter_value)

# Print the ID of the created global parameter
print("Created Global Parameter ID:", global_parameter_id)
