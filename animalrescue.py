"""
Creates root and opens the main window
"""
import tkinter as tk
import sqlite3
from modules.pages.mainpage import BuildMainWindow
from modules.othermodules.globals import Globals

# testing
# from modules.othermodules.filesandfolders import check_relative_folder
# print(check_relative_folder('images'))


# Connect to db
conn = sqlite3.connect('records/Records.db')

root = tk.Tk()                    # Create root
Globals.root = root
BuildMainWindow(root, conn)     # Launch main window


root.mainloop()             # Make program visible
conn.close()
