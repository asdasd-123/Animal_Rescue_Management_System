"""
Builds the main page of the rescue screen
"""
# Imports
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
import configparser
from TreeBuild import TreeBuild
from PIL import Image, ImageTk
from tkcalendar import Calendar
from datetime import datetime


class build_main_window():
    """Builds the main window"""
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self._setup_window()
        self._setup_fonts()
        self._setup_styles()
        self._setup_tabs()          # Setting up tabs (notebook) widget
        self._setup_tab_1_frames()  # Setting up tab1 (Dashboard) widgets
        self._setup_tab_1_widgets()

    def _setup_window(self):
        # Get and read config
        self.config = configparser.ConfigParser()
        self.config.read('Config/config.ini')

        # Set window title to name from config
        self.title = self.config['DEFAULT'].get('rescuename',
                                                'Rescue name not set up yet')
        wm_title = self.title
        self.master.wm_title(wm_title)

        # Set window size on launch
        self.master.geometry("1024x768")

    def _setup_fonts(self):
        # Title Font settings
        self.font_title = tkfont.Font(size=30, weight='bold')

        # Search box font
        self.font_search = tkfont.Font(size=12)

    def _setup_styles(self):
        # ==================
        # Testing Styles
        # ==================
        blue_frame = ttk.Style()
        blue_frame.configure("blue.TFrame", background="blue")
        green_frame = ttk.Style()
        green_frame.configure("green.TFrame", background="green")
        red_frame = ttk.Style()
        red_frame.configure("red.TFrame", background="red")
        yellow_frame = ttk.Style()
        yellow_frame.configure("yellow.TFrame", background="yellow")
        pink_frame = ttk.Style()
        pink_frame.configure("pink.TFrame", background="pink")
        brown_frame = ttk.Style()
        brown_frame.configure("brown.TFrame", background="brown")
        grey_frame = ttk.Style()
        grey_frame.configure("grey.TFrame", background="grey")
        purple_frame = ttk.Style()
        purple_frame.configure("purple.TFrame", background="purple")
        white_frame = ttk.Style()
        white_frame.configure("white.TFrame", background="white")
        blue_label = ttk.Style()
        blue_label.configure("blue.TLabel", background="blue")
        green_label = ttk.Style()
        green_label.configure("green.TLabel", background="green")
        red_label = ttk.Style()
        red_label.configure("red.TLabel", background="red")
        yellow_label = ttk.Style()
        yellow_label.configure("yellow.TLabel", background="yellow")
        pink_label = ttk.Style()
        pink_label.configure("pink.TLabel", background="pink")
        brown_label = ttk.Style()
        brown_label.configure("brown.TLabel", background="brown")
        grey_label = ttk.Style()
        grey_label.configure("grey.TLabel", background="grey")
        purple_label = ttk.Style()
        purple_label.configure("purple.TLabel", background="purple")
        white_label = ttk.Style()
        white_label.configure("white.TLabel", background="white")

        # ==================
        # Tab 1 (Dashboard) styles
        # ==================

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

    def _setup_tabs(self):
        note = ttk.Notebook(self.master)

        # Setup the tab frames
        self.tab1 = ttk.Frame(note)
        self.tab2 = ttk.Frame(note, style="tab2.TFrame")
        self.tab3 = ttk.Frame(note, style="tab3.TFrame")

        # Asign the above frames to tabs
        note.add(self.tab1, text="  Dashboard  ")
        note.add(self.tab2, text="Tab two")
        note.add(self.tab3, text="Tab three")

        # Packing the tabs widget to fill screen.
        note.pack(fill="both", expand=True)

    def _setup_tab_1_frames(self):
        # Header Frame. Contains Title, Logo, and tree-filters
        self.header = ttk.Frame(self.tab1)
        self.header.pack(side="top", fill="x")

        # - Logo Frame. Contains the logo picture
        self.logo_frame = ttk.Frame(self.header, width="150", height="160")
        self.logo_frame.pack_propagate(0)
        self.logo_frame.pack(side="right")

        # - Header/Filter Frame
        self.header_filter = ttk.Frame(self.header, padding="10")
        self.header_filter.pack(side="left", expand=True, fill="both")

        # -- Filters Frame
        self.filters_frame = ttk.LabelFrame(self.header_filter, text="Filters")
        self.filters_frame.pack(side="bottom", anchor="sw",
                                expand=True, fill="both")

        # -- Buttons Frame
        self.buttons_frame = ttk.LabelFrame(self.header_filter)
        self.buttons_frame.pack(side="bottom", anchor="sw",
                                expand=True, fill="both")

        # Tree/Search Frame
        self.tree_search_frame = ttk.Frame(self.tab1)
        self.tree_search_frame.pack(expand=True, fill="both")

    def _setup_tab_1_widgets(self):
        # -- Title Label
        title = ttk.Label(self.header_filter, text=self.title)
        title['font'] = self.font_title
        title.pack(side="top", anchor="w")

        # -- Load logo and create label for it
        logo_im = Image.open("catlogo.png")
        logo_ph = ImageTk.PhotoImage(logo_im)
        logo_img = ttk.Label(self.logo_frame, image=logo_ph)
        logo_img.image = logo_ph
        logo_img.pack(side="top")

        # Add new animal button
        animal_type = self.config['DEFAULT'].get('animaltype')
        add_new_button = ttk.Button(self.buttons_frame,
                                    text="Add New " + animal_type,
                                    command=self.add_new_animal_window)
        add_new_button.pack(side="left", anchor='nw', padx=6)

        # Add new medical entry button
        medical_entry_button = ttk.Button(
            self.buttons_frame,
            text="Add Medical Event",
            command=self.open_medical_entry_window)
        medical_entry_button.pack(side="left", anchor='nw', padx=6)

        # In Rescue checkbox
        self.in_rescue_var = tk.IntVar()
        self.in_rescue = ttk.Checkbutton(self.filters_frame,
                                         text="Only show animals in rescue: ",
                                         variable=self.in_rescue_var,
                                         command=self.refresh_main_tree)
        self.in_rescue.pack(side="left", anchor="w")
        self.in_rescue_var.set(1)

        # Get tree data and build tree (main data=md)
        md_query = "SELECT * FROM Main_Page_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = basic_db_query(self.conn, md_query)
        self.main_tree = TreeBuild(self.tree_search_frame,
                                   search=True,
                                   data=md[1],
                                   # widths=main_search_widths,
                                   headings=md[0])
        self.main_tree.tree.bind(
            "<Double-1>",
            lambda c: self.open_animal_window(
                self.main_tree.tree.item(self.main_tree.tree.focus())))

    def refresh_main_tree(self):
        md_query = "SELECT * FROM Main_Page_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = basic_db_query(self.conn, md_query)
        self.main_tree.refresh_data(md[1])

    def add_new_animal_window(self):
        animal_window(tk.Toplevel(self.master), self.conn, self,
                      window_type="new")

    def open_medical_entry_window(self):
        self.med_win = medical_entry_window(tk.Toplevel(self.master),
                                            self.conn, self)

    def open_animal_window(self, row_selected):
        animal_id = row_selected['values'][0]
        animal_window(tk.Toplevel(self.master), self.conn, self,
                      window_type="edit", animal_id=animal_id)


class medical_entry_window():
    def __init__(self, master, conn, main_win):
        self.conn = conn
        self.master = master
        self.master.withdraw()      # Hide window
        self.master.wm_title("Medical Entries")
        self.master.geometry("1024x700")
        self.main_win = main_win    # Used for comunicating with parent window.
        self._build_frames()
        self._build_widgets()
        self.master.deiconify()     # show window

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

    def _build_widgets(self):
        # - Add button
        self.add_button = ttk.Button(self.add_frame, text="Add Animal")
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
        md = basic_db_query(self.conn, animal_query)
        self.animal_tree = TreeBuild(self.animal_tree_frame,
                                     search=True,
                                     data=md[1],
                                     headings=md[0])

    def refresh_animal_data(self):
        md_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = basic_db_query(self.conn, md_query)
        self.animal_tree.refresh_data(md[1])


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
        self.left_frame = ttk.Frame(self.master, style="blue.TFrame")
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

    def _build_widgets(self):
        # - Title Labels
        self.id_label = ttk.Label(
            self.title_frame,
            font=self.font_title)
        self.id_label.pack(side="left", padx=5)
        self.name_entry = ttk.Entry(self.title_frame, font=self.font_title)
        self.name_entry.pack(side="left")

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


def basic_db_query(conn, query):
    """Runs SQL query on connection and returns results as list.
    list[0] = list of headings
    list[1] = list(column) of lists(rows) of data"""
    with conn:
        c = conn.cursor()
        c.execute(query)
        query_info = []
        query_info.append([desc[0] for desc in c.description])
        query_info.append(c.fetchall())
        return query_info


def adv_db_query(conn, query, dictionary, returnlist=True):
    """Runs SQL query on connection and returns results as list.
    list[0] = list of headings
    list[1] = list(column) of lists(rows) of data"""
    with conn:
        c = conn.cursor()
        c.execute(query, dictionary)
        if returnlist:
            query_info = []
            query_info.append([desc[0] for desc in c.description])
            query_info.append(c.fetchall())
            return query_info
        else:
            return


# def display_animal_window():
#     root_a.mainloop()
