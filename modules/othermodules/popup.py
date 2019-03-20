# =====================================
#   _____            _    _
#  |  __ \          | |  | |
#  | |__) ___  _ __ | |  | |_ __
#  |  ___/ _ \| '_ \| |  | | '_ \
#  | |  | (_) | |_) | |__| | |_) |
#  |_|   \___/| .__/ \____/| .__/
#             | |          | |
#             |_|          |_|
# =====================================
# Allows for the handling of multiple pop-up windows.
# Each one is asigned a window_id.
# If a popup with the specified window_id is already open, switch focus
# and update the text/header to the new info.

# Example use:
#   root = tk.Tk()

#   PopUp(root,                     Parent window
#         'window1',                window ID
#          text="text",             text in popup
#          heading="header text",   heading in popup
#          title="window title",    title of popup
#          center=False,            center window or not
#          size="200x200")          set size of window
import tkinter as tk
import tkinter.ttk as ttk


class __PopUpController__():
    """
    This is the controller class that handles which popups are open.
    DO NOT TOUCH
    """
    popup_dict = {}

    def _status(self, win_id):
        if win_id in self.popup_dict:
            if self.popup_dict[win_id][0] == 'open':
                return 'open'
        else:
            return 'not created'


class PopUp(__PopUpController__):
    def __init__(self, master, win_id, text="", heading="", title="",
                 center=True, size="480x300"):
        """
        Create a popup supplying the following info:
        * = optional
        master      - parent window
        win_id      - uniqueID of window
                    (if already exist, previous window will be updated)
        text*       - text in popup
        heading*    - heading in popup
        title*      - title of popup
        center*     - center window or not (default True)
        size*       - size of window
        """
        # Sort out args
        self.master = master
        self.text = text
        self.heading = heading
        self.size = size

        # Fetch status of desired window.
        status = super()._status(win_id)

        # Store the controller dictionary as class attr
        self.pop_dict = super().popup_dict

        # Decide on which function based on desired window status
        if status == 'open':
            self._update_text(win_id, text, heading)
        elif status == 'not created':
            self._setup_new_window(win_id)

        # Center the window
        if center:
            self._center_window(win_id)
        else:
            self.popup_dict[win_id][1].geometry(size)

        self.popup_dict[win_id][1].wm_title(title)

    def _setup_new_window(self, win_id):
        """
        Create a new popup window when the win_id is deemed to be new
        """
        # ==============
        # setup
        # ==============
        # Create new list to store window info
        self.pop_dict[win_id] = list(range(4))

        # Set status to open so if the popup is called again it will know
        self.pop_dict[win_id][0] = 'open'

        # Store the window toplevel in the PopUpController dictionary
        win = self.popup_dict[win_id][1] = tk.Toplevel(self.master)

        # ==============
        # Widgets and labels
        # ==============
        # Header label
        self.popup_dict[win_id][2] = ttk.Label(win, text=self.heading)
        self.popup_dict[win_id][2].pack(side="top", fill="x", anchor="n")

        # Ok button
        button = ttk.Button(win, text="OK",
                            command=lambda: self._on_closing(win_id))
        button.pack_propagate(0)
        button.pack(side="bottom", fill="x")

        # Text frame
        text_frame = ttk.Frame(win)
        text_frame.pack(side="top", anchor="n", fill="both", expand=True)

        # Text part
        text_scroll = tk.Scrollbar(text_frame)
        self.pop_dict[win_id][3] = tk.Text(text_frame)
        text_scroll.pack(side="right", fill="y")
        self.pop_dict[win_id][3].pack(side="left", fill="both", expand=True)
        text_scroll.config(command=self.pop_dict[win_id][3].yview)
        self.pop_dict[win_id][3].config(yscrollcommand=text_scroll.set)
        self.pop_dict[win_id][3].delete("1.0", 'end')
        self.pop_dict[win_id][3].insert("1.0", self.text)

        # ==============
        # set on-close protocol
        # ==============
        win.protocol("WM_DELETE_WINDOW", lambda: self._on_closing(win_id))

    def _on_closing(self, win_id):
        """
        When either the OK button is pressed or the top-right close button,
        this will destroy the window and wipe the ID from controller dictionary
        """
        self.pop_dict[win_id][1].destroy()
        del super().popup_dict[win_id]

    def _center_window(self, win_id):
        """
        Centers the selected window on the screen.
        """
        size = self.size.split("x")
        width = int(size[0])
        height = int(size[1])
        screen_width = self.popup_dict[win_id][1].winfo_screenwidth()
        screen_height = self.popup_dict[win_id][1].winfo_screenheight()

        # work  out coords
        y = (screen_height/2) - (height/2)
        x = (screen_width/2) - (width/2)

        self.popup_dict[win_id][1].geometry(
            '%dx%d+%d+%d' % (width, height, x, y - 40))

    def _update_text(self, win_id, text, heading):
        """
        Updates the text for the popup if it already exists and is open.
        Will also force the focus back to the popup
        """
        if text != '':
            self.pop_dict[win_id][3].delete("1.0", 'end')
            self.pop_dict[win_id][3].insert("1.0", str(text))
        if heading != '':
            self.pop_dict[win_id][2]['text'] = str(heading) + "\n"

        self.pop_dict[win_id][3].lift()
        self.pop_dict[win_id][3].focus_force()
