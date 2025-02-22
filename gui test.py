import tkinter as tk
import os

# def button_click():
#     print("Button clicked!")

# window = tk.Tk()
# window.title("My GUI")

# button = tk.Button(window, text="Click Me!", command=button_click)
# button.pack()

# window.mainloop() 

# filepath = "/home/eet3tz/Project_Repo/Projects/"
# bakepath = os.path.join("/home/eet3tz/Project_Repo/Projects/" , "bakeSettings.json")
# print(bakepath)

 # Command parameters
output_cfg = 2
output_type = 0
heat_ohms = 2
max_current = 0
max_output_current = 0.12
heater_display = 1
terminator = "\n"

command = f"HTRSET {output_cfg},{output_type},{heat_ohms},{max_current},{max_output_current},{heater_display}{terminator}"
print(command)

