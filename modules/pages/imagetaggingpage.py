"""
Image Tagging Page:

Used to asign photo's to specified animals.
When asignment is made, pull across and rename photo's to avoid overlap,
and store asignments in DB
"""
from modules.othermodules.tk_window import CenterWindow
from modules.othermodules.treebuild import TreeBuild
from modules.othermodules.sqlitefunctions import BasicDbQuery
import tkinter as tk
import tkinter.ttk as ttk


class ImageTaggingWindow():
    def __init__(self, master, conn, main_win):
        # Init variable setup
        self.master = master
        self.conn = conn
        self.main_win = main_win
        self.animal_dict = {}       # Dictionary of row IDs and animal ID's
        #                             for adding animals to the list.

        # Window setup
        self.master.wm_title("Image Tagging")
        CenterWindow(self.master)

        # Build window
        self._build_frames()
        self._build_widgets()

    def _build_frames(self):
        # Right Frame
        self.right_frame = ttk.Frame(self.master, width="250")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="y")

        # - In-Rescue checkbox frame
        self.in_rescue_frame = ttk.Frame(self.right_frame)
        self.in_rescue_frame.pack(side="top", fill="x", anchor="w")

        # - Animal tree frame
        self.animal_tree_frame = ttk.Frame(self.right_frame)
        self.animal_tree_frame.pack(side="top", fill="both", expand=True)

        # Main frame
        main_frame = ttk.Frame(self.master, style="blue.TFrame")
        main_frame.pack(side="left", fill="both", expand=True)

        # - Header frame
        self.header_frame = ttk.Frame(main_frame)
        self.header_frame.pack(side="top", fill="x")

        # - Data frame
        data_frame = ttk.Frame(main_frame)
        data_frame.pack(side="top", fill="both", expand=True)

        # -- Animals column
        self.animal_frame = ttk.Frame(data_frame, width="200")
        self.animal_frame.pack(side="right", fill="both", ipadx="20")
        self.animal_frame.pack_propagate(0)

        # -- Image holder frame (image and buttons)
        self.image_holder = ttk.Frame(data_frame)
        self.image_holder.pack(side="left", fill="both", expand=True)

        # --- Photo buttons frame
        self.photo_buttons_frame = ttk.Frame(self.image_holder, height="100",)
        self.photo_buttons_frame.pack_propagate(0)
        self.photo_buttons_frame.pack(side="bottom", fill="x")

        # --- Photo Frame
        self.photo_frame = ttk.Frame(self.image_holder)
        self.photo_frame.pack(side="top", fill="both", expand=True)

    def _build_widgets(self):
        # =============
        # Right frame
        # =============
        # In-Rescue checkbox
        self.in_rescue_var = tk.IntVar()
        self.in_rescue = ttk.Checkbutton(self.in_rescue_frame,
                                         text="Only show animals in rescue: ",
                                         variable=self.in_rescue_var,
                                         command=self.refresh_animal_data)
        self.in_rescue.pack(side="left", anchor="w")
        self.in_rescue_var.set(1)

        # Build animal tree.
        animal_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            animal_query += "_Active"
        md = BasicDbQuery(self.conn, animal_query)
        self.animal_tree = TreeBuild(self.animal_tree_frame,
                                     search=True,
                                     data=md[1],
                                     widths=[35, 300],
                                     headings=md[0])
        self.animal_tree.tree.bind(
            "<Double-1>",
            lambda c: self._add_animal())

        # Close button
        close_button = ttk.Button(self.right_frame,
                                  text="Cancel",
                                  command=lambda: self.close_window())
        # close_button.pack_propagate(0)
        close_button.pack(side="bottom", fill="x", anchor="s")

        # =============
        # Header frame
        # =============
        # Title
        heading = ttk.Label(self.header_frame, text="Image Tagging",
                            font=self.main_win.font_title)
        heading.pack(side="left", anchor="nw", padx=10, pady=10)

        # =============
        # Photo buttons frame
        # =============
        previous_button = ttk.Button(self.photo_buttons_frame,
                                     text="<-----", style="img.TButton")
        previous_button.pack_propagate(0)
        previous_button.pack(side="left", fill="both", expand="true",
                             padx=10, pady=10)
        tag_photo = ttk.Button(self.photo_buttons_frame,
                               text="Tag", style="img.TButton")
        tag_photo.pack_propagate(0)
        tag_photo.pack(side="left", fill="both", expand="true",
                       padx=10, pady=10)
        del_photo = ttk.Button(self.photo_buttons_frame,
                               text="Delete", style="img.TButton")
        del_photo.pack_propagate(0)
        del_photo.pack(side="left", fill="both", expand="true",
                       padx=10, pady=10)
        open_photo = ttk.Button(self.photo_buttons_frame,
                                text="Open", style="img.TButton")
        open_photo.pack_propagate(0)
        open_photo.pack(side="left", fill="both", expand="true",
                        padx=10, pady=10)
        next_button = ttk.Button(self.photo_buttons_frame,
                                 text="----->", style="img.TButton")
        next_button.pack_propagate(0)
        next_button.pack(side="left", fill="both", expand="true",
                         padx=10, pady=10)

    def refresh_animal_data(self):
        md_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = BasicDbQuery(self.conn, md_query)
        self.animal_tree.refresh_data(md[1])

    def _add_animal(self):
        tree = self.animal_tree.tree

        # Check if anything selected in tree. Return if nothing
        results = tree.item(tree.focus())['values']
        if results == '':
            return
        # Save selected item in tree
        animal_id = results[0]
        add_name = results[1]

        # Check if animal already in list. If it is, return
        if animal_id in self.animal_dict.values():
            return

        # Get next available row id (for if animals are rmeoved and readded)
        button_id = self._get_next_row_id()  # returns 999 if already exist
        if button_id == 999:
            return
        else:
            self.animal_dict[button_id] = animal_id

        # ===========
        # Build the actual visible row now.
        # ===========
        # Short string of button id to make the below simpler
        ids = str(button_id)

        # Create a new master frame for row
        setattr(self, "rowmasterf" + ids, ttk.Frame(self.animal_frame))

        # Set as local var so canbe used below without being a mess
        masterf = getattr(self, "rowmasterf" + ids)
        masterf.pack(side="top", fill="x", ipady=1, padx=10)

        # Create the widgets:
        # The remove button
        setattr(self, "rowb" + ids, ttk.Button(
            masterf,
            text="-",
            width="2",
            command=lambda: self._remove_animal(button_id)))
        getattr(self, "rowb" + ids).pack(side="left")

        # The label
        setattr(self, "rowl" + ids, ttk.Label(
            masterf,
            text=str(animal_id) + ": " + add_name))
        getattr(self, "rowl" + ids).pack(side="left")

    def _get_next_row_id(self):
        for i in range(16):     # Max 16 entries
            if i not in self.animal_dict:
                return i
        return 999

    def _remove_animal(self, rem_id):
        ids = str(rem_id)
        getattr(self, "rowmasterf" + ids).destroy()
        del self.animal_dict[rem_id]

    def close_window(self):
        self.master.destroy()
