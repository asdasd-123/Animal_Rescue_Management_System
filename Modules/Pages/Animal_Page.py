"""
Animal Page:

This page handles the displaying and editing of an animals information.
It shows the following:
 - Data from the Animals table in the db (name, colour, dob etc)
 - Medical history in a treeview
 - Homing history in a treeview
"""
import tkinter.ttk as ttk
import tkinter.font as tkfont
import tkinter as tk
from tkcalendar import Calendar
from Modules.Other_modules.SQLite_functions import (basic_db_query,
                                                    adv_db_query)
from Modules.Other_modules.TreeBuild import TreeBuild
from datetime import datetime


class animal_window():
    def __init__(self, master, conn, main_win,
                 window_type="new", animal_id=""):
        self.conn = conn
        self.master = master
        self.master.withdraw()      # Hide window
        self.master.geometry("1680x900")
        self.animal_id = animal_id
        self.main_win = main_win
        self.type = window_type
        self._Setup_fonts()
        self._build_frames()
        self._build_widgets()
        if animal_id != "" and window_type == "edit":
            self._populate_data(conn, self.animal_id)
        self.master.deiconify()     # Show window

    def _Setup_fonts(self):
        # Title Font settings
        self.font_title = tkfont.Font(size=30, weight='bold')

    def _build_frames(self):
        # Right Frame
        self.right_frame = ttk.Frame(self.master, width="300",
                                     style="green.TFrame")
        self.right_frame.pack(side="right", fill="both")

        # - Image frame
        self.image_frame = ttk.Frame(self.right_frame, width="300",
                                     height="300", style="grey.TLabel")
        self.image_frame.pack(side="top", fill="x")

        # - Notes header frame
        self.note_header_frame = ttk.Frame(self.right_frame)
        self.note_header_frame.pack(side="top", fill="x")

        # - Notes frame
        self.notes_frame = ttk.Frame(self.right_frame)
        self.notes_frame.pack(side="top", fill="both", anchor="n")

        # - Buttons frame
        self.buttons_frame = ttk.Frame(self.right_frame)
        self.buttons_frame.pack(side="bottom", expand=True,
                                fill="x", anchor="s")

        # -- Left button frame
        self.left_button_frame = ttk.Frame(self.buttons_frame)
        self.left_button_frame.pack(side="left", expand=True,
                                    fill="both", anchor="w")

        # -- Right button frame
        self.right_button_frame = ttk.Frame(self.buttons_frame)
        self.right_button_frame.pack(side="right", expand=True,
                                     fill="both", anchor="e")

        # Left frame
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.pack(side="left", expand=True, fill="both")

        # - Title frame
        self.title_frame = ttk.Frame(self.left_frame)
        self.title_frame.pack(side="top", fill="x", ipady=10)

        # - Data frame (for dob, colour etc)
        self.data_frame = ttk.Frame(self.left_frame)
        self.data_frame.pack(side="top", fill="x")

        # -- Setting column list
        self.data_col = []
        # -- Column setup
        self.col_padd = 5
        self.col_paddl = self.col_padd + 1
        num_of_cols = 2     # Increase to add columns.
        for col in range(num_of_cols):
            self.data_col.insert(col, [0, 1])
            self.data_col[col][0] = ttk.Frame(self.data_frame)
            self.data_col[col][0].pack(side="left", ipadx=5, anchor="n")
            self.data_col[col][1] = ttk.Frame(self.data_frame)
            self.data_col[col][1].pack(side="left", ipadx=5, anchor="n")

        # -- Dob column
        self.dob_col = ttk.Frame(self.data_frame)
        self.dob_col.pack(side="left", ipadx=5, anchor="n")

        # --- Dob known holding frame
        self.dob_holding_frame = ttk.Frame(self.dob_col)
        self.dob_holding_frame.pack(side="top", anchor="n", fill="x")
        # ---- Dob known frames
        self.dob_known_col = [0, 1]
        self.dob_known_col[0] = ttk.Frame(self.dob_holding_frame)
        self.dob_known_col[0].pack(side="left", ipadx=5, anchor="n")
        self.dob_known_col[1] = ttk.Frame(self.dob_holding_frame)
        self.dob_known_col[1].pack(side="left", ipadx=5, anchor="n")

        # - Central frame
        self.central_frame = ttk.Frame(self.left_frame, style="brown.TFrame")
        self.central_frame.pack(side="top", fill="both", expand=True)

        # -- Medical history frame
        self.med_hist_frame = ttk.Frame(self.central_frame)
        self.med_hist_frame.pack(side="left", fill="both")

        # -- homing history frame
        self.home_hist_frame = ttk.Frame(self.central_frame)
        self.home_hist_frame.pack(side="left", fill="both")

    def _build_widgets(self):
        # ===============
        # Title widgets
        # ===============
        # - Title Labels
        self.id_label = ttk.Label(
            self.title_frame,
            font=self.font_title)
        self.id_label.pack(side="left", padx=5)
        self.name_entry = ttk.Entry(self.title_frame, font=self.font_title)
        self.name_entry.pack(side="left")

        # ===============
        # Right frame, notes widgets
        # ===============
        # - Notes items.
        # - Notes label
        self.notes_l = ttk.Label(self.note_header_frame,
                                 text="Notes:", anchor="n")
        self.notes_l.pack(side="top", fill="x",)

        # - Notes text box
        notes_scroll = tk.Scrollbar(self.notes_frame)
        self.note_text = tk.Text(self.notes_frame, width="34")
        notes_scroll.pack(side="right", fill="y", expand=True)
        self.note_text.pack(side="right", fill="both", expand=True)
        notes_scroll.config(command=self.note_text.yview)
        self.note_text.config(yscrollcommand=notes_scroll.set)

        # ===============
        # animal data widgets
        # ===============
        # - Column 0 items
        # - Colour
        self.colour_0 = ttk.Label(self.data_col[0][0], text="Colour: ")
        self.colour_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.colour_1 = ttk.Entry(self.data_col[0][1])
        self.colour_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Sex
        self.sex_0 = ttk.Label(self.data_col[0][0], text="Sex: ", anchor="w")
        self.sex_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.sex_1 = ttk.Combobox(self.data_col[0][1], state='readonly',
                                  values=('Unknown', 'Male', 'Female'))
        self.sex_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Chip number
        self.chip_num_0 = ttk.Label(self.data_col[0][0], text="Chip Number: ")
        self.chip_num_0.pack(side="top", anchor="w", ipady=self.col_padd)
        self.chip_num_1 = ttk.Entry(self.data_col[0][1])
        self.chip_num_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Hair type
        self.hair_type_0 = ttk.Label(self.data_col[0][0],
                                     text="Hair type: ", anchor="w")
        self.hair_type_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.hair_type_1 = ttk.Combobox(self.data_col[0][1], state='readonly',
                                        values=('Short Hair', 'Long Hair'))
        self.hair_type_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - In Rescue
        self.in_rescue_0 = ttk.Label(self.data_col[0][0],
                                     text="In Rescue: ", anchor="w")
        self.in_rescue_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.in_rescue_var = tk.IntVar()
        self.in_rescue_1 = ttk.Checkbutton(self.data_col[0][1],
                                           variable=self.in_rescue_var)
        self.in_rescue_1.pack(side="top", anchor="w", pady=self.col_padd)
        self.in_rescue_var.set(1)

        # - Dob columns
        # - DOB known
        self.dob_known_0 = ttk.Label(self.dob_known_col[0],
                                     text="DOB known?: ", anchor="w")
        self.dob_known_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.dob_known_1 = ttk.Combobox(self.dob_known_col[1],
                                        state='readonly',
                                        values=('No', 'Yes', 'Roughly'))
        self.dob_known_1.pack(side="top", anchor="w", pady=self.col_padd)
        self.dob_known_1.bind("<<ComboboxSelected>>", self._show_hide_date)

        # - DOB text
        self.dob_text_0 = ttk.Label(self.dob_known_col[0],
                                    text="Date of birth: ", anchor="w")
        self.dob_text_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.dob_text_1 = ttk.Label(self.dob_known_col[1], anchor="w")
        self.dob_text_1.pack(side="top", anchor="w", ipady=self.col_padd)

        # DOB Cal
        self.dob_cal = Calendar(self.dob_col)
        self.dob_cal.pack(side="top", anchor="n", fill="x")

        # ===============
        # Medical history widgets
        # ===============
        # Medical history label
        sql_query = f"""
                    SELECT SUM(Cost)
                    FROM Medical
                    where Animal_ID = {self.animal_id}
                    """
        med_spend = basic_db_query(self.conn, sql_query)[1][0][0]
        med_spend = round(med_spend, 2)
        med_text = f"Medical History   -   Total Spend = £{med_spend}"
        med_label = ttk.Label(self.med_hist_frame, text=med_text)
        med_label['font'] = self.main_win.font_sub_title
        med_label.pack(side="top", fill="x")

        # Get medical history data from view
        sql_query = """SELECT *
                    FROM Animal_Page_Med_History
                    WHERE Animal_ID = :ID"""
        sql_dict = {'ID': self.animal_id}
        med_results = adv_db_query(self.conn, sql_query, sql_dict)
        med_tree = TreeBuild(self.med_hist_frame,
                             search=True,
                             data=med_results[1],
                             widths=[0, 100, 50, 500],
                             headings=med_results[0])

        # ===============
        # Homing history widgets
        # ===============
        # Medical history label
        home_label = ttk.Label(self.home_hist_frame,
                               text="Homing History (Temp Data)")
        home_label['font'] = self.main_win.font_sub_title
        home_label.pack(side="top", fill="x")

        # Temp table
        hom_tree = TreeBuild(self.home_hist_frame,
                             search=True,
                             data=med_results[1],
                             widths=[0, 100, 50, 700],
                             headings=med_results[0])
        # ===============
        # bottom-right save/submit widgets
        # ===============
        # Cancel / submit / save changes buttons
        self.cancel = ttk.Button(self.right_button_frame, text="Cancel",
                                 command=self.close_window)
        self.cancel.pack(side="left", anchor="w", padx=20, pady=10)
        self.submit = ttk.Button(
            self.left_button_frame,
            text="Submit",
            command=lambda c="save": self.update_database(c))
        self.save = ttk.Button(
            self.left_button_frame,
            text="Save",
            command=lambda c="edit": self.update_database(c))

        if self.type == "edit":
            self.save.pack(side="right", anchor="e", padx=20, pady=10)
        else:
            self.submit.pack(side="right", anchor="e", padx=20, pady=10)

    def update_database(self, sql_type=""):
        if sql_type == "":
            print("no sql type supplied")
            return

        update_dict = {}

        # Get values
        update_dict['Name'] = self.name_entry.get().rstrip()
        update_dict['Colour'] = self.colour_1.get().rstrip()
        update_dict['Sex'] = self.sex_1.get()
        update_dict['Chip'] = self.chip_num_1.get().rstrip()
        update_dict['Hair'] = self.hair_type_1.get()
        update_dict['DobKnown'] = self.dob_known_1.get()
        if update_dict['DobKnown'] != "No":
            temp_date = datetime.strptime(self.dob_cal.get_date(), '%d/%m/%Y')
            temp_date = temp_date.strftime('%Y-%m-%d')
        else:
            temp_date = ""
        update_dict['Dob'] = temp_date
        update_dict['Notes'] = self.note_text.get('1.0', 'end').rstrip()
        update_dict['InRescue'] = self.in_rescue_var.get()
        if sql_type == "edit":
            update_dict['ID'] = self.id_label.cget('text')
            sql_query = """UPDATE Animal
                       SET Name = :Name,
                       Chip_Num = :Chip,
                       Date_Of_Birth = :Dob,
                       DOB_Known = :DobKnown,
                       Sex = :Sex,
                       Colour = :Colour,
                       Hair_Type = :Hair,
                       Notes = :Notes,
                       In_Rescue = :InRescue
                       WHERE ID = :ID"""

            adv_db_query(self.conn, sql_query, update_dict, returnlist=False)
        elif sql_type == "save":
            next_id_qry = """SELECT ID FROM Animal ORDER BY ID DESC LIMIT 1"""
            next_id_returns = basic_db_query(self.conn, next_id_qry)
            next_id = int(next_id_returns[1][0][0]) + 1
            update_dict['ID'] = next_id
            sql_query = """INSERT INTO Animal (
                        Name,
                        Chip_Num,
                        Date_Of_Birth,
                        DOB_Known,
                        Sex,
                        Colour,
                        Hair_Type,
                        Notes,
                        In_Rescue)
                        VALUES (
                        :Name,
                        :Chip,
                        :Dob,
                        :DobKnown,
                        :Sex,
                        :Colour,
                        :Hair,
                        :Notes,
                        :InRescue
                        )"""
            adv_db_query(self.conn, sql_query, update_dict, returnlist=False)

        self.close_window()
        self.main_win.refresh_main_tree()

    def close_window(self):
        self.master.destroy()

    def _show_hide_date(self, event):
        option = self.dob_known_1.get()
        if option in ("Yes", "Roughly"):
            self.dob_cal.pack(side="top", anchor="n", fill="x")
        else:
            self.dob_cal.pack_forget()

    def _populate_data(self, conn, id):
        populate_query = "SELECT * FROM Populate_Animal_Data WHERE ID = :ID"
        populate_dict = {'ID': id}
        results = adv_db_query(conn, populate_query, populate_dict)

        # Update widgets
        # ID
        id_text = results[1][0][results[0].index('ID')]
        self.id_label.configure(text=id_text)

        # Name
        name_text = results[1][0][results[0].index('Name')]
        self.name_entry.insert(0, name_text)

        # Chip num
        chip_num_text = results[1][0][results[0].index('Chip_Num')]
        self.chip_num_1.insert(0, chip_num_text)

        # DOB known
        dob_known_text = results[1][0][results[0].index('DOB_Known')]
        self.dob_known_1.set(dob_known_text)
        self._show_hide_date("")

        # Date of birth
        if dob_known_text != "No":
            dob_text = results[1][0][results[0].index('Date_Of_Birth')]
            new_date = datetime.strptime(dob_text, '%Y-%m-%d')
            new_date_text = new_date.strftime('%d/%m/%Y')
            self.dob_cal.selection_set(new_date)
            self.dob_text_1.configure(text=new_date_text)

        # Sex
        sex_text = results[1][0][results[0].index('Sex')]
        self.sex_1.set(sex_text)

        # Colour
        colour_text = results[1][0][results[0].index('Colour')]
        self.colour_1.insert(0, colour_text)

        # Hair type
        hair_type_text = results[1][0][results[0].index('Hair_Type')]
        self.hair_type_1.set(hair_type_text)

        # Notes
        notes_text = results[1][0][results[0].index('Notes')]
        self.note_text.insert('end', notes_text)

        # In rescue
        in_rescue_value = results[1][0][results[0].index('In_Rescue')]
        self.in_rescue_var.set(in_rescue_value)
