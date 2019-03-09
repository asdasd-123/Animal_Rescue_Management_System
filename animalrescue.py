"""
Creates root and opens the main window
"""
import tkinter as tk
import sqlite3
from modules.pages.mainpage import BuildMainWindow


# Connect to db
conn = sqlite3.connect('records/Records.db')

root = tk.Tk()                    # Create root
BuildMainWindow(root, conn)     # Launch main window


root.mainloop()             # Make program visible
conn.close()
