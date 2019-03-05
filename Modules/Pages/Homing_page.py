"""
Homing Page:

This page will be used when homing an animal to a new owner.
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar
from Modules.Other_modules.SQLite_functions import (basic_db_query)
from Modules.Other_modules.TreeBuild import TreeBuild


class homing_window():
    def __init__(self, master, conn, main_win):
        # Init variable setup
        self.master = master
        self.conn = conn
        self.main_win = main_win
        self.animal_dict = {}       # Dictionary of row IDs and animal ID's
        #                             for adding animals to the list.

        # Window setup
        self.master.wm_title("Homing")
        self.master.geometry("1024x700")

        # Build the window
        self._build_frames()
        self._build_widgets()

    def _build_frames(self):
        # Right frame
        right_frame = ttk.Frame(self.master, width="250")
        right_frame.pack_propagate(0)
        right_frame.pack(side="right", fill="y")

        # - Calendar frame
        self.cal_frame = ttk.Frame(right_frame)
        self.cal_frame.pack(side="top")

        # - Add button frame
        self.add_frame = ttk.Frame(right_frame)
        self.add_frame.pack(side="top", fill="x")

        # - In-Rescue checkbox frame
        self.in_rescue_frame = ttk.Frame(right_frame)
        self.in_rescue_frame.pack(side="top", fill="x", anchor="w")

        # - Animal tree frame
        self.animal_tree_frame = ttk.Frame(right_frame)
        self.animal_tree_frame.pack(side="top", fill="both", expand=True)

        # - Add/Cancel buttons frame
        self.buttons_frame = ttk.Frame(right_frame)
        self.buttons_frame.pack(side="top",
                                fill="x", anchor="s")

        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(side="left", fill="both", expand=True)

        # - Header frame
        self.header_frame = ttk.Frame(main_frame)
        self.header_frame.pack(side="top", fill="x")

        # - Data frame
        data_frame = ttk.Frame(main_frame)
        data_frame.pack(side="top", fill="both", expand=True)

        # -- Setting column list for inputs
        self.data_col = []
        # -- Column setup
        self.col_padd = 5
        self.col_paddl = self.col_padd + 1
        num_of_cols = 1     # Increase to add columns.
        for col in range(num_of_cols):
            self.data_col.insert(col, [0, 1])
            self.data_col[col][0] = ttk.Frame(data_frame)
            self.data_col[col][0].pack(side="left", fill="y", ipadx=5, anchor="n")
            self.data_col[col][1] = ttk.Frame(data_frame)
            self.data_col[col][1].pack(side="left", fill="y", ipadx=5, anchor="n")
        
        # -- Notes column
        note_frame = ttk.Frame(data_frame)
        note_frame.pack(side="left", fill="both", expand=True, padx=2)

        # --- Notes header frame
        self.note_header_frame = ttk.Frame(note_frame)
        self.note_header_frame.pack(side="top", fill="x")

        # --- Notes frame
        self.notes_frame = ttk.Frame(note_frame)
        self.notes_frame.pack(side="top", fill="both", anchor="n", expand=True)
        self.notes_frame.pack_propagate(0)

        # -- Animals column
        self.animal_frame = ttk.Frame(data_frame, width="200")
        self.animal_frame.pack(side="left", fill="both")
        self.animal_frame.pack_propagate(0)

    def _build_widgets(self):
        # =============
        # Right frame
        # =============
        # Calendar
        self.calendar = Calendar(self.cal_frame)
        self.calendar.pack(side="top", anchor="n")

        # Add button
        self.add_button = ttk.Button(self.add_frame, text="Add Animal", command=self._add_animal)
        self.add_button.pack(side="top", anchor="n", fill="x")

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
        md = basic_db_query(self.conn, animal_query)
        self.animal_tree = TreeBuild(self.animal_tree_frame,
                                     search=True,
                                     data=md[1],
                                     widths=[35, 300],
                                     headings=md[0])
        self.animal_tree.tree.bind(
            "<Double-1>",
            lambda c: self._add_animal())

        # cancel / submit button
        self.submit = ttk.Button(self.buttons_frame, text="Submit")
        self.submit.pack(side="left", fill="x")
        self.cancel = ttk.Button(self.buttons_frame, text="Cancel",
                                 command=self.close_window)
        self.cancel.pack(side="right", fill="x")

        # =============
        # Header frame
        # =============
        # Title
        heading = ttk.Label(self.header_frame, text="Collections / Adoptions",
                            font=self.main_win.font_title)
        heading.pack(side="left", anchor="nw", padx=10, pady=10)

        # =============
        # Column 0/1 Contents frame
        # =============

        # Homing or adoption radio button
        type_label = ttk.Label(self.data_col[0][0], text="Collection/Homing")
        type_label.pack(side="top", fill="x", pady=self.col_paddl)
        spacer = ttk.Label(self.data_col[0][0], text="")
        spacer.pack(side="top", fill="x", pady=self.col_paddl)
        self.home_type = ''
        self.radio_home = ttk.Radiobutton(self.data_col[0][1], value="home", text="Home to new owner", variable=self.home_type)
        self.radio_home.pack(side="top", fill="x", pady=self.col_padd)
        self.radio_home.invoke()
        self.radio_collect = ttk.Radiobutton(self.data_col[0][1], value="collect", text="Taking into the rescue", variable=self.home_type)
        self.radio_collect.pack(side="top", fill="x", pady=self.col_padd)

        # Name
        name_l = ttk.Label(self.data_col[0][0], text="Name")
        name_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.name_e = ttk.Entry(self.data_col[0][1])
        self.name_e.pack(side="top", fill="x", pady=self.col_padd)
        
        # Address 1
        address1_l = ttk.Label(self.data_col[0][0], text="Address line 1")
        address1_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.address1_e = ttk.Entry(self.data_col[0][1])
        self.address1_e.pack(side="top", fill="x", pady=self.col_padd)

        # Address 2
        address2_l = ttk.Label(self.data_col[0][0], text="Address line 2")
        address2_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.address2_e = ttk.Entry(self.data_col[0][1])
        self.address2_e.pack(side="top", fill="x", pady=self.col_padd)

        # Town
        town_l = ttk.Label(self.data_col[0][0], text="Town")
        town_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.town_e = ttk.Entry(self.data_col[0][1])
        self.town_e.pack(side="top", fill="x", pady=self.col_padd)

        # County
        county_l = ttk.Label(self.data_col[0][0], text="County 1")
        county_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.county_e = ttk.Entry(self.data_col[0][1])
        self.county_e.pack(side="top", fill="x", pady=self.col_padd)

        # Postcode
        postcode_l = ttk.Label(self.data_col[0][0], text="Postcode")
        postcode_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.postcode_e = ttk.Entry(self.data_col[0][1])
        self.postcode_e.pack(side="top", fill="x", pady=self.col_padd)

        # Phone number
        phone_num_l = ttk.Label(self.data_col[0][0], text="Phone Number")
        phone_num_l.pack(side="top", fill="x", ipady=self.col_paddl)
        self.phone_num_e = ttk.Entry(self.data_col[0][1])
        self.phone_num_e.pack(side="top", fill="x", pady=self.col_padd)

        # =============
        # notes frame frame
        # =============
        # - Notes items.
        # - Notes label
        self.notes_l = ttk.Label(self.note_header_frame,
                                 text="Notes:", anchor="n")
        self.notes_l.pack(side="top", fill="x")

        # - Notes text box
        text_scroll = tk.Scrollbar(self.notes_frame)
        self.text_box = tk.Text(self.notes_frame)
        text_scroll.pack(side="right", fill="y")
        self.text_box.pack(side="right", fill="y")
        text_scroll.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=text_scroll.set)

        # =============
        # Animal frame
        # =============
        self.animal_l = ttk.Label(self.animal_frame,
                                  text="Animals to process:", anchor="n")
        self.animal_l.pack(side="top", fill="x")

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

        #  Get next available row id (for if animals are removed and readded)
        button_id = self._get_next_row_id()     # returns 999 if already exist
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

        # set as local var so can be used below without being a mess
        masterf = getattr(self, "rowmasterf" + ids)
        masterf.pack(side="top", fill="x", ipady=1)

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

    def _remove_animal(self, rem_id):
        ids = str(rem_id)
        getattr(self, "rowmasterf" + ids).destroy()
        del self.animal_dict[rem_id]    

    def _get_next_row_id(self):
        for i in range(16):     # Max 16 entries
            if i not in self.animal_dict:
                return i
        return 999

    def refresh_animal_data(self):
        md_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = basic_db_query(self.conn, md_query)
        self.animal_tree.refresh_data(md[1])

    def close_window(self):
        self.master.destroy()
