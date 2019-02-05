"""
Builds the main page of the rescue screen
"""
# Imports
import tkinter
# Import tkinter.font
# import tkinter.ttk as ttk
import configparser

root = tkinter.Tk()


class build_main_page(object):
    def __init__(self):
        self._Setup_window()
        self._Setup_tabs()
        root.mainloop()

    def _Setup_window(self):
        # Get and read config
        config = configparser.ConfigParser()
        config.read('Config/config.ini')
        root_wm_title = config['DEFAULT'].get('rescuename',
                                              'Rescue name not set up yet')
        root.wm_title(root_wm_title)
        root.geometry("1024x768")

    def _Setup_tabs(self):
        print("test")
