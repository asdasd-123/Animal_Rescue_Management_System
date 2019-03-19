"""
Medical Page:

Used for submitting medical events for animals currently in the rescue.
Multiple cats can be entered at once up to 15.

Future wishlist:
Create some form of grid instead to space out all the options more clearly
when adding multiple animals.
"""
import tkinter as tk
import tkinter.ttk as ttk
from modules.othermodules.sqlitefunctions import (BasicDbQuery,
                                                  AdvDbQuery)
from modules.othermodules.treebuild import TreeBuild
from modules.othermodules.dateentry import DateEntry
from datetime import datetime, timedelta
from tkcalendar import Calendar
from modules.othermodules.old_popup import PopUpWindow
from modules.othermodules.tk_window import CenterWindow


class MedicalEntryWindow():
    def __init__(self, master, conn, main_win):
        self.conn = conn
        self.master = master
        self.med_dict = {}          # dictionary of button ID's and animal ids
        self.master.withdraw()      # Hide window
        self.master.wm_title("Medical Entries")
        CenterWindow(self.master)
        self.main_win = main_win    # Used for comunicating with parent window.
        self._build_frames()
        self._build_widgets()
        self.master.deiconify()     # show window
        self.popup = False  # Check used later to see if popup created.

    def _build_frames(self):
        # Right frame
        self.right_frame = ttk.Frame(self.master, width="200")
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="y")

        # - Add button frame
        self.add_frame = ttk.Frame(self.right_frame)
        self.add_frame.pack(side="top", fill="x")

        # - In-Rescue checkbox frame
        self.in_rescue_frame = ttk.Frame(self.right_frame)
        self.in_rescue_frame.pack(side="top", fill="x", anchor="w")

        # - Animal tree frame
        self.animal_tree_frame = ttk.Frame(self.right_frame)
        self.animal_tree_frame.pack(side="top", fill="both", expand="True")

        # - Add/Cancel buttons frame
        self.buttons_frame = ttk.Frame(self.right_frame)
        self.buttons_frame.pack(side="bottom", expand=True,
                                fill="x", anchor="s")

        # Left frame
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # - Header frame
        self.header_frame = ttk.Frame(self.left_frame)
        self.header_frame.pack(side="top", anchor="w", fill="x")

        # -- Calender frame
        self.cal_frame = ttk.Frame(self.header_frame, width="300")
        self.cal_frame.pack(side="right", fill="y")

        # - Medical entries frame
        self.med_frame = ttk.Frame(self.left_frame)
        self.med_frame.pack(side="top", fill="both", expand=True)

    def _build_widgets(self):
        # Right frame items
        # - Add button
        self.add_button = ttk.Button(self.add_frame, text="Add Animal",
                                     command=self._add_animal)
        self.add_button.pack(side="top", anchor="n", fill="x")

        # - In-Rescue checkbox
        self.in_rescue_var = tk.IntVar()
        self.in_rescue = ttk.Checkbutton(self.in_rescue_frame,
                                         text="Only show animals in rescue: ",
                                         variable=self.in_rescue_var,
                                         command=self.refresh_animal_data)
        self.in_rescue.pack(side="left", anchor="w")
        self.in_rescue_var.set(1)

        # - Build animal tree.
        animal_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            animal_query += "_Active"
        md = BasicDbQuery(self.conn, animal_query)
        self.animal_tree = TreeBuild(self.animal_tree_frame,
                                     search=True,
                                     data=md[1],
                                     headings=md[0])
        self.animal_tree.tree.bind(
            "<Double-1>",
            lambda c: self._add_animal())

        # cancel / submit button
        self.submit = ttk.Button(self.buttons_frame, text="Submit",
                                 command=self._submit_records)
        self.submit.pack(side="left", fill="x")
        self.cancel = ttk.Button(self.buttons_frame, text="Cancel",
                                 command=self.close_window)
        self.cancel.pack(side="right", fill="x")

        # Header frame items
        # - heading label
        heading = ttk.Label(self.header_frame, text="Medical Entries",
                            font=self.main_win.font_title)
        heading.pack(side="left", anchor="nw", padx=10)

        # -- Calendar frame items
        # -- Calandar
        self.calendar = Calendar(self.cal_frame)
        self.calendar.pack(side="top", anchor="n")

    def _add_animal(self):
        tree = self.animal_tree.tree
        results = tree.item(tree.focus())['values']
        if results == '':
            return
        animal_id = results[0]
        add_name = results[1]

        # Sort out next buttons/frame ID
        button_id = self._get_next_row_id()     # returns 999 if maxed out
        if button_id == 999:
            return
        else:
            self.med_dict[button_id] = animal_id

        # String of button id and shortening name for creating attributes
        ids = str(button_id)
        # ================ Frames
        # Create new master framer for row
        setattr(self, "medmasterf" + ids, ttk.Frame(self.med_frame,
                                                    style="grey.TFrame"))
        # set as local var so can be used below
        medmasterf = getattr(self, "medmasterf" + ids)
        getattr(self, "medmasterf" + ids).pack(side="top", fill="x", ipady=1)
        # - Create top frame
        setattr(self, "medf" + ids, ttk.Frame(medmasterf))
        # set as local var so can be used below
        medf = getattr(self, "medf" + ids)
        getattr(self, "medf" + ids).pack(side="top", fill="x")
        # - Create 2nd frame
        setattr(self, "medf2" + ids, ttk.Frame(medmasterf))
        # set as local var so can be used below
        medf2 = getattr(self, "medf2" + ids)
        getattr(self, "medf2" + ids).pack(side="top", fill="x")

        # ================ Widgets
        # Create the button
        setattr(self, "medb" + ids, ttk.Button(
            medf,
            text="-",
            width="2",
            command=lambda: self._remove_animal(button_id)))
        getattr(self, "medb" + ids).pack(side="left")

        # Create Labels
        setattr(self, "medid" + ids, ttk.Label(medf, text=animal_id))
        getattr(self, "medid" + ids).pack(side="left")
        name_text = ": " + add_name + " | "
        setattr(self, "medname" + ids, ttk.Label(medf, text=name_text))
        getattr(self, "medname" + ids).pack(side="left")
        # Used when building error log on submission.
        setattr(self, "mednametext" + ids, add_name)

        # Med_type combobox
        setattr(self, "medtype" + ids, ttk.Combobox(medf, state="readonly",
                                                    values=("Vet", "Other")))
        getattr(self, "medtype" + ids).pack(side="left")
        getattr(self, "medtype" + ids).bind(
            "<<ComboboxSelected>>",
            lambda c: self._med_type_selection(button_id))

        # - (vet() Vet_Name label/combobox
        text = "| Vet Name : "
        setattr(self, "medvetnamel" + ids, ttk.Label(medf, text=text))
        vet_text = self.main_win.config['DEFAULT'].get('defaultvet')
        setattr(self, "medvetnamee" + ids, ttk.Entry(medf))
        getattr(self, "medvetnamee" + ids).insert(0, vet_text)

        # - (vet) Op type
        setattr(self, "medoptypel" + ids, ttk.Label(medf, text="| Type : "))
        setattr(self, "medoptype" + ids, ttk.Combobox(
            medf,
            state="readonly",
            values=("Chip", "Checkup", "Neuter", "Vaccination", "Other")))
        getattr(self, "medoptype" + ids).bind(
            "<<ComboboxSelected>>",
            lambda c: self._op_type_selection(button_id))

        # -- (chip) chiplabel/num
        setattr(self, "chipnuml" + ids, ttk.Label(medf, text="| Chip Num : "))
        setattr(self, "chipnume" + ids, ttk.Entry(medf))

        # Cost entry boxs *Movable and will be destoyed in certain routes.
        #                  re-create when needed.
        setattr(self, "medcostl" + ids, ttk.Label(medf, text="| Cost : "))
        setattr(self, "medcoste" + ids, ttk.Entry(medf))

        # Checkup Label
        text = "| Checkup Notes : "
        setattr(self, "medcheckupl" + ids, ttk.Label(medf2, text=text))

        # Notes Entry/label
        setattr(self, "mednotesl" + ids, ttk.Label(medf2, text="| Notes : "))
        setattr(self, "mednotese" + ids, ttk.Entry(medf2))

        # Other op type label/entry
        text = "| Procedure : "
        setattr(self, "medotheropl" + ids, ttk.Label(medf, text=text))
        setattr(self, "medotherope" + ids, ttk.Entry(medf))

        # vac type (first/second)
        text = "| Vac Type : "
        setattr(self, "medvactypel" + ids, ttk.Label(medf, text=text))
        setattr(self, "medvactype" + ids, ttk.Combobox(
            medf,
            state="readonly",
            values=("First", "Second", "Top-Up")))
        getattr(self, "medvactype" + ids).bind(
            "<<ComboboxSelected>>",
            lambda c: self._vac_type_selection(button_id))

        # vac due date + label
        text = "| Next Vac Due (YYYY-MM-DD) : "
        setattr(self, "medduedatel" + ids, ttk.Label(medf2, text=text))
        setattr(self, "medduedate" + ids, DateEntry(medf2))

        # Worm/Flea/Both label + combo
        text = "| Treatment : "
        setattr(self, "medfleatypel" + ids, ttk.Label(medf, text=text))
        setattr(self, "medfleatype" + ids, ttk.Combobox(
            medf,
            state="readonly",
            values=("Flea", "Worming", "Flea and Worming", "Other")))
        getattr(self, "medfleatype" + ids).bind(
            "<<ComboboxSelected>>",
            lambda c: self._non_vet_type_selection(button_id))

    def _get_next_row_id(self):
        for i in range(16):     # Max 30 entries
            if i not in self.med_dict:
                return i
        return 999

    def _remove_animal(self, rem_id):
        ids = str(rem_id)
        getattr(self, "medmasterf" + ids).destroy()
        del self.med_dict[rem_id]

    # =========
    # Functions for controlling row contents when options selected
    # =========
    def _med_type_selection(self, button_id):
        ids = str(button_id)
        option = getattr(self, "medtype" + ids).get()
        # unpack everything first :
        getattr(self, "medvetnamel" + ids).pack_forget()
        getattr(self, "medvetnamee" + ids).pack_forget()
        getattr(self, "medoptypel" + ids).pack_forget()
        getattr(self, "medoptype" + ids).set("")    # trigger op_type below
        getattr(self, "medoptype" + ids).event_generate("<<ComboboxSelected>>")
        getattr(self, "medoptype" + ids).pack_forget()
        getattr(self, "medfleatypel" + ids).pack_forget()
        getattr(self, "medfleatype" + ids).pack_forget()

        if option == "Vet":
            # Pack vet options
            getattr(self, "medvetnamel" + ids).pack(side="left")
            getattr(self, "medvetnamee" + ids).pack(side="left")
            getattr(self, "medoptypel" + ids).pack(side="left")
            getattr(self, "medoptype" + ids).pack(side="left")
        elif option == "Other":
            getattr(self, "medfleatypel" + ids).pack(side="left")
            getattr(self, "medfleatype" + ids).pack(side="left")

    def _op_type_selection(self, button_id):
        ids = str(button_id)
        option = getattr(self, "medoptype" + ids).get()
        medf = getattr(self, "medf" + ids)
        medf2 = getattr(self, "medf2" + ids)
        # unpack everything first
        getattr(self, "chipnuml" + ids).pack_forget()
        getattr(self, "chipnume" + ids).pack_forget()
        getattr(self, "medcostl" + ids).pack_forget()
        getattr(self, "medcheckupl" + ids).pack_forget()
        getattr(self, "mednotese" + ids).pack_forget()
        getattr(self, "mednotesl" + ids).pack_forget()
        getattr(self, "medotheropl" + ids).pack_forget()
        getattr(self, "medotherope" + ids).pack_forget()
        getattr(self, "medvactype" + ids).set("")    # trigger op_type below
        getattr(self, "medvactype" + ids).event_generate(
            "<<ComboboxSelected>>")
        getattr(self, "medvactype" + ids).pack_forget()
        getattr(self, "medvactypel" + ids).pack_forget()
        # destroy items that need to be moved
        getattr(self, "medcostl" + ids).destroy()
        getattr(self, "medcoste" + ids).destroy()
        medf2.pack_forget()

        if option == "Chip":
            # only pack the frame if needed
            medf2.pack(side="top", fill="x")
            getattr(self, "chipnuml" + ids).pack(side="left")
            getattr(self, "chipnume" + ids).pack(side="left")
            # re-create it in 2nd row
            setattr(self, "medcostl" + ids, ttk.Label(medf2, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf2))
            getattr(self, "medcoste" + ids).pack(side="left")
        elif option == "Checkup":
            setattr(self, "medcostl" + ids, ttk.Label(medf, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf))
            getattr(self, "medcoste" + ids).pack(side="left")
            # only pack the frame if needed
            medf2.pack(side="top", fill="x")
            getattr(self, "medcheckupl" + ids).pack(side="left")
            getattr(self, "mednotese" + ids).pack(side="left",
                                                  fill="x",
                                                  expand=True)
        elif option == "Neuter":
            setattr(self, "medcostl" + ids, ttk.Label(medf, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf))
            getattr(self, "medcoste" + ids).pack(side="left")
        elif option == "Other":
            getattr(self, "medotheropl" + ids).pack(side="left")
            getattr(self, "medotherope" + ids).pack(side="left",
                                                    fill="x",
                                                    expand=True)
            # only pack the frame if needed
            medf2.pack(side="top", fill="x")
            setattr(self, "medcostl" + ids, ttk.Label(medf2, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf2))
            getattr(self, "medcoste" + ids).pack(side="left")
            getattr(self, "mednotesl" + ids).pack(side="left")
            getattr(self, "mednotese" + ids).pack(side="left",
                                                  fill="x",
                                                  expand=True)
        elif option == "Vaccination":
            getattr(self, "medvactypel" + ids).pack(side="left")
            getattr(self, "medvactype" + ids).pack(side="left")

    def _vac_type_selection(self, button_id):
        ids = str(button_id)
        option = getattr(self, "medvactype" + ids).get()
        medf2 = getattr(self, "medf2" + ids)
        # unpack everything first
        getattr(self, "medduedate" + ids).pack_forget()
        getattr(self, "medduedatel" + ids).pack_forget()
        getattr(self, "medcostl" + ids).destroy()
        getattr(self, "medcoste" + ids).destroy()
        medf2.pack_forget()

        if option in ("First", "Second", "Top-Up"):
            # only pack the frame if needed
            medf2.pack(side="top", fill="x")
            setattr(self, "medcostl" + ids, ttk.Label(medf2, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf2))
            getattr(self, "medcoste" + ids).pack(side="left")
            getattr(self, "medduedatel" + ids).pack(side="left")
            getattr(self, "medduedate" + ids).pack(side="left")
        # Inserting Dates into datebox.
        due_date_text = datetime.strptime(self.calendar.get_date(), '%d/%m/%Y')
        if option == "First":
            due_date_text += timedelta(days=28)
            due_date_text = due_date_text.strftime('%Y-%m-%d')
            getattr(self, "medduedate" + ids).delete(0, 'end')
            getattr(self, "medduedate" + ids).insert(0, due_date_text)
        elif option in ("Second", "Top-Up"):
            due_date_text += timedelta(days=365)
            due_date_text = due_date_text.strftime('%Y-%m-%d')
            getattr(self, "medduedate" + ids).delete(0, 'end')
            getattr(self, "medduedate" + ids).insert(0, due_date_text)

    def _non_vet_type_selection(self, button_id):
        ids = str(button_id)
        option = getattr(self, "medfleatype" + ids).get()
        medf = getattr(self, "medf" + ids)
        # unpack everything first
        getattr(self, "medcostl" + ids).destroy()
        getattr(self, "medcoste" + ids).destroy()
        getattr(self, "medotheropl" + ids).pack_forget()
        getattr(self, "medotherope" + ids).pack_forget()

        if option in ('Flea', 'Worming', 'Flea and Worming'):
            setattr(self, "medcostl" + ids, ttk.Label(medf, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf))
            getattr(self, "medcoste" + ids).pack(side="left")
        elif option == "Other":
            getattr(self, "medotheropl" + ids).pack(side="left")
            getattr(self, "medotherope" + ids).pack(side="left")
            setattr(self, "medcostl" + ids, ttk.Label(medf, text="| Cost : "))
            getattr(self, "medcostl" + ids).pack(side="left")
            setattr(self, "medcoste" + ids, ttk.Entry(medf))
            getattr(self, "medcoste" + ids).pack(side="left")
    # =========
    # End of functions
    # =========

    def _submit_records(self):
        if not self._check_errors() or len(self.med_dict) == 0:
            return

        # =============
        # Building up the dictionary used to generate SQL
        # =============
        date = self.calendar.get_date()
        date = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
        for k, v in self.med_dict.items():
            # get initial values
            animal_id = int(v)
            ids = str(k)        # widget ID as STR for getting values
            value_dict = {}     # empty dict used to contain values for SQL

            # Set chip-update flag to false
            chip_update = False

            # Add Animal
            value_dict['Animal_ID'] = animal_id

            # Add Date
            value_dict['Date'] = date

            # - Check first combobox Vet/Other
            combo = getattr(self, "medtype" + ids).get()
            if combo == "Vet":
                value_dict['Medical_Type'] = combo
                # Add VetName
                vetname = getattr(self, "medvetnamee" + ids).get()
                value_dict['Vet_Name'] = vetname

                # Check vet appointment type
                app_type = getattr(self, "medoptype" + ids).get()
                if app_type == "Chip":
                    # Add Medical Type:
                    value_dict['Procedure'] = app_type

                    # enable chip updating after medical entry
                    chip_update = True

                    # Add chip number
                    chip_num = getattr(self, "chipnume" + ids).get()
                    value_dict['Chip_Num'] = chip_num

                    # Add Cost
                    cost = getattr(self, "medcoste" + ids).get()
                    value_dict['Cost'] = float(cost)

                # If Checkup
                elif app_type == "Checkup":
                    # Add Medical Type:
                    value_dict['Procedure'] = app_type

                    # Add Cost
                    cost = getattr(self, "medcoste" + ids).get()
                    value_dict['Cost'] = float(cost)

                    # Add Notes
                    notes = getattr(self, "mednotese" + ids).get()
                    value_dict['Notes'] = notes

                # If Neuter
                elif app_type == "Neuter":
                    # Add Medical Type:
                    value_dict['Procedure'] = app_type

                    # Add Cost
                    cost = getattr(self, "medcoste" + ids).get()
                    value_dict['Cost'] = float(cost)

                # If Other
                elif app_type == "Other":
                    # Add Medical Type:
                    procedure = getattr(self, "medotherope" + ids).get()
                    value_dict['Procedure'] = procedure

                    # Add Cost
                    cost = getattr(self, "medcoste" + ids).get()
                    value_dict['Cost'] = float(cost)

                    # Add Notes
                    notes = getattr(self, "mednotese" + ids).get()
                    value_dict['Notes'] = notes

                # If vaccination
                elif app_type == "Vaccination":
                    # Add Medical Type:
                    procedure = "Vaccination"
                    value_dict['Procedure'] = procedure

                    # vac-type
                    vac_type = getattr(self, "medvactype" + ids).get()
                    if vac_type == 'First':
                        value_dict['Vac_Type'] = 1
                    elif vac_type == 'Second':
                        value_dict['Vac_Type'] = 2
                    elif vac_type == 'Top-Up':
                        value_dict['Vac_Type'] = 3

                    # Add Cost
                    cost = getattr(self, "medcoste" + ids).get()
                    value_dict['Cost'] = float(cost)

                    # Due date
                    due_date = getattr(self, "medduedate" + ids).get_date()
                    due_date = due_date.strftime('%Y-%m-%d')
                    value_dict['Due_Date'] = due_date

            # If Other
            elif combo == "Other":
                value_dict['Medical_Type'] = combo

                # Add Cost
                cost = getattr(self, "medcoste" + ids).get()
                value_dict['Cost'] = float(cost)

                # Check other-type box
                othertype = getattr(self, "medfleatype" + ids).get()
                if othertype in ('Flea', 'Worming', 'Flea and Worming'):
                    value_dict['Procedure'] = othertype

                elif othertype == 'Other':
                    procedure = getattr(self, "medotherope" + ids).get()
                    value_dict['Procedure'] = procedure

            # =============
            # Using Dictionary to generate insert str
            # =============
            sqlstr = 'INSERT INTO Medical (\n'
            # Adding column names
            for k, v in value_dict.items():
                sqlstr += str(k) + ',\n'
            sqlstr = sqlstr[:len(sqlstr) - 2]   # remove final command&newline

            sqlstr += ')\nVALUES (\n'

            # Adding value headings.
            for k, v in value_dict.items():
                sqlstr += ':' + str(k) + ',\n'
            sqlstr = sqlstr[:len(sqlstr) - 2]   # remove final command&newline

            sqlstr += ')'
            AdvDbQuery(self.conn, sqlstr, value_dict, returnlist=False)

            # =============
            # Updating chip info if necesarry
            # =============
            if chip_update:
                sqlstr = """
                         UPDATE Animal
                         SET Chip_Num = :Chip_Num
                         WHERE ID = :ID
                         """

                chip_dict = {}
                chip_dict['Chip_Num'] = chip_num
                chip_dict['ID'] = animal_id
                AdvDbQuery(self.conn, sqlstr, chip_dict, returnlist=False)
            self.main_win.refresh_main_tree()
        self.close_window()

    def close_window(self):
        self.master.destroy()

    def refresh_animal_data(self):
        md_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = BasicDbQuery(self.conn, md_query)
        self.animal_tree.refresh_data(md[1])

    def _check_errors(self):
        """Returns True if no errors found.
        Otherwise returns False and opens a pop-up box with errors found"""
        error = False
        err_text = ''
        for row, key in enumerate(self.med_dict):
            # get initial values
            rownum = row + 1
            ids = str(key)                                      # row-ID
            animal_name = getattr(self, "mednametext" + ids)    # Animal Name

            # row-error variables.
            row_error = False
            row_error_header = f"Row {rownum}: Errors Found ({animal_name})\n"
            row_error_text = ''

            # - Check first combobox Vet/Other
            combo = getattr(self, "medtype" + ids).get()
            if combo == "Vet":
                # Check if VetName supplied
                vetname = getattr(self, "medvetnamee" + ids).get()
                if vetname == '':
                    row_error = True
                    row_error_text += '  -  Vet name missing\n'

                # Check vet appointment type
                app_type = getattr(self, "medoptype" + ids).get()
                # If blank
                if app_type == "":
                    row_error = True
                    row_error_text += '  -  Select an appointment type\n'
                # If Chip Num
                elif app_type == "Chip":
                    # Check chip number
                    chip_num = getattr(self, "chipnume" + ids).get()
                    if chip_num == '':
                        row_error = True
                        row_error_text += '  -  Enter the chip number\n'
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0)\n'
                # If Checkup
                elif app_type == "Checkup":
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0)\n'
                # If Neuter
                elif app_type == "Neuter":
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0)\n'
                # If Other
                elif app_type == "Other":
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0)\n'
                    # Check Procedure
                    procedure = getattr(self, "medotherope" + ids).get()
                    if procedure == '':
                        row_error = True
                        row_error_text += '  -  Enter a procedure\n'
                # If vaccination
                elif app_type == "Vaccination":
                    # Check vac-type box
                    vac_type = getattr(self, "medvactype" + ids).get()
                    if vac_type == '':
                        row_error = True
                        row_error_text += '  -  Select a vaccination type\n'
                    else:
                        # Check cost
                        cost = getattr(self, "medcoste" + ids).get()
                        if cost == '':
                            row_error = True
                            row_error_text += '  -  Enter a cost (even 0)\n'
                        # Check Date is valid
                        valid_date = getattr(self, "medduedate" + ids).is_valid
                        if not valid_date:
                            row_error = True
                            row_error_text += '  -  Enter a valid date\n'
            # If Other
            elif combo == "Other":
                # Check other-type combobox
                # If blank
                othertype = getattr(self, "medfleatype" + ids).get()
                if othertype == '':
                    row_error = True
                    row_error_text += '  -  Pick a treatment type\n'
                # if Flear or worming
                elif othertype in ('Flea', 'Worming', 'Flea and Worming'):
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0 is ok)\n'
                elif othertype == 'Other':
                    # Check cost
                    cost = getattr(self, "medcoste" + ids).get()
                    if cost == '':
                        row_error = True
                        row_error_text += '  -  Enter a cost (even 0 is ok)\n'
                    # Check Procedure
                    procedure = getattr(self, "medotherope" + ids).get()
                    if procedure == '':
                        row_error = True
                        row_error_text += '  -  Enter the procedure\n'
            elif combo == "":
                row_error = True
                row_error_text += '  -  Select an item in the drop-down box\n'

            # If errors have been detected. add the error text to the log.
            if row_error:
                error = True
                err_text += row_error_header + row_error_text + '\n'
        if error:
            self.open_popup_window(heading="Errors found in entries",
                                   text=err_text)
            return False
        else:
            return True

    def open_popup_window(self, heading, text):
        if self.popup is False:
            self.popup = PopUpWindow(tk.Toplevel(self.master),
                                     heading=heading,
                                     text=text,
                                     main_win=self)
            self.popup.text_box.lift()
            self.popup.text_box.focus_force()
        else:
            self.popup.replace_text(text=text)
            self.popup.text_box.lift()
            self.popup.text_box.focus_force()
