"""
Creates root and opens the main window
"""
import tkinter as tk
import sqlite3
from Modules.Pages.Main_page import build_main_window


# Connect to db
conn = sqlite3.connect('Records/Records.db')

root = tk.Tk()                    # Create root
build_main_window(root, conn)     # Launch main window


root.mainloop()             # Make program visible
conn.close()
