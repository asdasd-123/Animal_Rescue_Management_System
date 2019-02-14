import tkinter as tk
import sqlite3
from GUI_Main_page import build_main_window


# Connect to db
conn = sqlite3.connect('Records/Records.db')

root = tk.Tk()                    # Create root
build_main_window(root, conn)     # Launch main window
# animal_window(tk.Toplevel(root), "0001 : Example Test Here")


root.mainloop()             # Make program visible
conn.close()
