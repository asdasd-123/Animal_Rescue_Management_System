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
# This library makes generating popups in tkinter a lot less tedius.
#
# The types of popup are as follows:
#  -  PopUpWindow 
#     Intended to be used to force only one copy of the window to stay open.
#     As such, it requires a variable in the parent class.
#
#  -  BasicPopUpWindow
#     No features. Just a textbox popup that can be called and requires no
#     communicaton to the parent window.


import tkinter as tk
import tkinter.ttk as ttk


class PopUpWindow():
    def __init__(self, master, main_win, size="480x300",
                 heading="", text=""):
        self.master = master
        self.size = size
        self.heading = heading + '\n'
        self.text = text
        self.main_win = main_win
        self.master.geometry(size)
        self._build_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        self.main_win.popup = 'not created'
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
