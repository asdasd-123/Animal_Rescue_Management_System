#   _____        _       ______       _
#  |  __ \      | |     |  ____|     | |
#  | |  | | __ _| |_ ___| |__   _ __ | |_ _ __ _   _
#  | |  | |/ _` | __/ _ \  __| | '_ \| __| '__| | | |
#  | |__| | (_| | ||  __/ |____| | | | |_| |  | |_| |
#  |_____/ \__,_|\__\___|______|_| |_|\__|_|   \__, |
#                                               __/ |
#                                              |___/

# A ttk widget extention to allow date inputting with validation and retrieval.
# Contains option for either grey-filling it with text that will dissappear or
# actuall pre-filling the date.
#
# ===================================
# Example of how to create the widget.
# ===================================
# root = tk.TK()
# date1 = DateEntry(root, prefill=False, text="Enter Date Here: YYYY-MM-DD")
# date2 = DateEntry(root, prefill=True, text="2019-02-19")
#
# ===================================
# How to retrieve data from the widget.
# ===================================
# Get the full date as a datetime object:
# full_date = date1.get_date()
#
# Year, Month, and Day:
# year = date1.year
# month = date1.month
# day = date1.day
#
# ===================================
# How to check is date in box is valid.
# ===================================
# if date1.is_valid:
#     print("date1 is valid")


import tkinter.ttk as ttk
from datetime import datetime


class DateEntry(ttk.Entry):
    def __init__(self, master, prefill=False, text="YYYY-MM-DD", **kwargs):
        """set prefill=True if the text needs to stay after
        clicking into the box"""
        ttk.Entry.__init__(self, master, **kwargs)
        self.master = master
        self.text = text
        self.prefill = prefill
        self.bind('<FocusIn>', self._focus_in)
        self.bind('<FocusOut>', self._focus_out)
        self.insert(0, text)
        self.configure(foreground='grey')

    def _focus_in(self, event=None):
        if self.text == self.get() and not self.prefill:
            self.delete(0, 'end')
        self.configure(foreground='black')

    def _focus_out(self, event=None):
        if self.get() == '':
            self.configure(foreground='grey')
            self.insert(0, self.text)
            return

        date_valid = True
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            date_valid = False

        if date_valid:
            self.configure(foreground='black')
        else:
            # need to re-input data to get rid of any potential highlighting.
            temp_text = self.get()
            self.delete(0, 'end')
            self.insert(0, temp_text)
            self.configure(foreground='red')

    @property
    def is_valid(self):
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def get_date(self):
        if self.is_valid:
            return datetime.strptime(self.get(), '%Y-%m-%d')

    @property
    def year(self):
        if self.is_valid:
            return self.get()[0:4]

    @property
    def month(self):
        if self.is_valid:
            return self.get()[5:7]

    @property
    def day(self):
        if self.is_valid:
            return self.get()[8:]