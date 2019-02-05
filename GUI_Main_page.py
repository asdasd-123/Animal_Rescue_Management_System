"""
Builds the main page of the rescue screen
"""
# Imports
import tkinter
# Import tkinter.font
import tkinter.ttk as ttk
import configparser

root = tkinter.Tk()


class Build_main_window(object):
    def __init__(self):
        self._Setup_window()
        self._Setup_styles()
        self._Setup_tabs()
        self._Setup_tab_1()

    def _Setup_window(self):
        # Get and read config
        config = configparser.ConfigParser()
        config.read('Config/config.ini')
        root_wm_title = config['DEFAULT'].get('rescuename',
                                              'Rescue name not set up yet')
        root.wm_title(root_wm_title)
        root.geometry("1024x768")

    def _Setup_styles(self):
        # ==================
        # Tab 1 styles
        # ==================
        # Tab1 Style
        tab1_style = ttk.Style()
        tab1_style.configure("tab1.TFrame", background="green")

        # ==================
        # Tab 2 styles
        # ==================
        # Tab2 Style
        tab2_style = ttk.Style()
        tab2_style.configure("tab2.TFrame", background="red")

        # ==================
        # Tab 3 styles
        # ==================
        # Tab3 Style
        tab3_style = ttk.Style()
        tab3_style.configure("tab3.TFrame", background="blue")

    def _Setup_tabs(self):
        note = ttk.Notebook(root)

        # Setup the tab frames
        tab1 = ttk.Frame(note, style="tab1.TFrame")
        tab2 = ttk.Frame(note, style="tab2.TFrame")
        tab3 = ttk.Frame(note, style="tab3.TFrame")

        # Asign the above frames to tabs
        note.add(tab1, text="Tab one")
        note.add(tab2, text="Tab two")
        note.add(tab3, text="Tab three")

        # Packing the note.
        note.pack(fill="both", expand=True)

    def _Setup_tab_1(self):
        print("setting up tab 1")


def Display_main_window():
    root.mainloop()
