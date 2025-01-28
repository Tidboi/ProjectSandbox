import tkinter as tk
import os

def button_click():
    print("Button clicked!")

window = tk.Tk()
window.title("My GUI")

button = tk.Button(window, text="Click Me!", command=button_click)
button.pack()

window.mainloop() 

# filepath = "/home/eet3tz/Project_Repo/Projects/"
# bakepath = os.path.join("/home/eet3tz/Project_Repo/Projects/" , "bakeSettings.json")
# print(bakepath)


