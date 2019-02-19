import tkinter as tk
import tkinter.ttk as ttk
from DateEntry import DateEntry

root = tk.Tk()                    # Create root

blue_frame = ttk.Style()
blue_frame.configure("blue.TFrame", background="blue")

test_frame = ttk.Frame(root, width=200, height=200, style="blue.TFrame")
test_frame.pack_propagate(0)
test_frame.pack(side="top")

date = DateEntry(test_frame)
date.pack()

root.mainloop()
