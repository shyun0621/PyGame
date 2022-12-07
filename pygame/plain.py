# importing easygui module
from easygui import *
from Tkinter import Tk

# calculate window position
root = Tk()
pos = int(root.winfo_screenwidth() * 0.5), int(root.winfo_screenheight() * 0.2)
root.withdraw()
rootWindowPosition = "+%d+%d" % pos

# patch rootWindowPosition
easygui.rootWindowPosition = rootWindowPosition

# message to be displayed
text = "Enter the following details"

# window title
title = "Custom Cycle Generation"

# list of multiple inputs
input_list = ["Fill amount (gal)", "Wash time (min)", "Spin time (min)", "Rinse time (min)"]

# list of default text
default_list = ["2", "30", "60", "30"]

# creating a integer box
output = multenterbox(text, title, input_list, default_list)

# title for the message box
title = "Generated Custom Cycle"

# creating a message
message = "Entered details are in form of list : " + str(output)

# creating a message box
msg = msgbox(message, title)