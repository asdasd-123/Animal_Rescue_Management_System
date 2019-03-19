# =====================================
#   _____            _    _
#  |  __ \          | |  | |
#  | |__) ___  _ __ | |  | |_ __  ___
#  |  ___/ _ \| '_ \| |  | | '_ \/ __|
#  | |  | (_) | |_) | |__| | |_) \__ \
#  |_|   \___/| .__/ \____/| .__/|___/
#             | |          | |
#             |_|          |_|
# =====================================
# Used to make temporary popup windows in tkinter less tedius
#
# The types of popup are as follows:
#  -  PopUpWindow
#         Forces only one copy of the window to stay open.
#         As such, it requires a class attribute to be setup called "popup".
#         Due to the attribute, only one popup can be linked to each class.
#         Has now been replaced by AdvPopUpWindow (which allows user to specify
#         which variable to use to store window info in it.)
#
#         Example usage:
#         class Temp():
#             def __init__(self):
#                 self.popup = False
#
#             def open_popup()
#                 if not self.popup:
#                     PopUpWindow
#
#  -  BasicPopUpWindow
#         No features. Just a textbox popup that can be called and requires no
#         communicaton to the parent window.
#
#         Example usage:
#         BasicPopUpWindow(tk.Toplevel(self.master),
#                          heading="Medical Entry",
#                          text=results_string,
#                          size="200x200")
#


import tkinter as tk
import tkinter.ttk as ttk


class PopUpWindow():
    def __init__(self, master, main_win, size="480x300",
                 heading="", text=""):
        self.master = master
        self.size = size
        self.heading = heading + '\n'
        self.text = text
        self.main_class = main_win  # The class that holds the "exists" var
        self.master.geometry(size)
        self._build_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        self.main_class.popup = False
        self.master.destroy()

    def _build_widgets(self):
        # Header label
        self.header = ttk.Label(self.master, text=self.heading)
        self.header.pack(side="top", fill="x", anchor="n")

        # Ok button
        button = ttk.Button(self.master, text="OK",
                            command=lambda: self._on_closing())
        button.pack_propagate(0)
        button.pack(side="bottom", fill="x")

        # Text frame
        text_frame = ttk.Frame(self.master)
        text_frame.pack(side="top", anchor="n", fill="both", expand=True)

        # Text part
        text_scroll = tk.Scrollbar(text_frame)
        self.text_box = tk.Text(text_frame)
        text_scroll.pack(side="right", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=text_scroll.set)
        self.text_box.delete("1.0", 'end')
        self.text_box.insert("1.0", self.text)

    def replace_text(self, heading='', text=''):
        if text != '':
            self.text_box.delete("1.0", 'end')
            self.text_box.insert("1.0", str(text))
        if heading != '':
            self.header['text'] = str(heading) + "\n"


class BasicPopUpWindow():
    def __init__(self, master, size="480x300",
                 heading="", text=""):
        self.master = master            # The Toplevel
        self.heading = heading + '\n'
        self.text = text

        self.master.geometry(size)  # Set window size
        self._build_widgets()       # Build the widgets

        # Set function to run on exit of window.
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        self.master.destroy()

    def _build_widgets(self):
        # header label
        self.header = ttk.Label(self.master, text=self.heading)
        self.header.pack(side="top", fill="x", anchor="n")

        # Ok button
        button = ttk.Button(self.master, text="OK",
                            command=lambda: self._on_closing())
        button.pack_propagate(0)
        button.pack(side="bottom", fill="x")

        # Text frame
        text_frame = ttk.Frame(self.master)
        text_frame.pack(side="top", anchor="n", fill="both", expand=True)

        # Text part
        text_scroll = tk.Scrollbar(text_frame)
        self.text_box = tk.Text(text_frame)
        text_scroll.pack(side="right", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=text_scroll.set)
        self.text_box.delete("1.0", 'end')
        self.text_box.insert("1.0", self.text)


class AdvPopUpWindow():
    def __init__(self, master, main_var_class, var,  size="480x300",
                 heading="", text=""):
        self.size = size
        self.heading = heading + '\n'
        self.text = text
        self.main_class = main_var_class
        self.main_var = var

        # check if win already built
        if not hasattr(self.main_class, self.main_var):
            created = False
        else:
            created = True

        if created is False:
            self.master = tk.Toplevel(master)
            setattr(self.main_class, self.main_var, self.master)
            self._first_time_setup()
        else:
            print(f"Already Open {self.main_var}")
            self.master = getattr(self.main_class, self.main_var)
            self._second_time_setup()

        self.master.geometry(size)

    def _first_time_setup(self):
        self._build_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _second_time_setup(self):
        self.replace_text(heading=self.heading, text=self.text)
        self.text_box.lift()
        self.text_box.focus_force()

    def _on_closing(self):
        self.main_class.popup = False
        self.master.destroy()
        setattr(self.main_class, self.main_var, False)

    def _build_widgets(self):
        # Header label
        self.header = ttk.Label(self.master, text=self.heading)
        self.header.pack(side="top", fill="x", anchor="n")

        # Ok button
        button = ttk.Button(self.master, text="OK",
                            command=lambda: self._on_closing())
        button.pack_propagate(0)
        button.pack(side="bottom", fill="x")

        # Text frame
        text_frame = ttk.Frame(self.master)
        text_frame.pack(side="top", anchor="n", fill="both", expand=True)

        # Text part
        text_scroll = tk.Scrollbar(text_frame)
        self.text_box = tk.Text(text_frame)
        text_scroll.pack(side="right", fill="y")
        self.text_box.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=text_scroll.set)
        self.text_box.delete("1.0", 'end')
        self.text_box.insert("1.0", self.text)

    def replace_text(self, heading='', text=''):
        if text != '':
            self.text_box.delete("1.0", 'end')
            self.text_box.insert("1.0", str(text))
        if heading != '':
            self.header['text'] = str(heading) + "\n"
