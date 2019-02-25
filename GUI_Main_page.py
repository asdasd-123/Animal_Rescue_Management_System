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
from DateEntry import DateEntry
from datetime import datetime
from datetime import timedelta


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
        logo_im = Image.open("logo.png")
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
                self.main_tree.tree.item(self.main_tree.tree.focus()), c))

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

    def open_animal_window(self, row_selected, event=None):
        region = self.main_tree.tree.identify("region", event.x, event.y)
        if region != "heading":
            animal_id = row_selected['values'][0]
            animal_window(tk.Toplevel(self.master), self.conn, self,
                          window_type="edit", animal_id=animal_id)


class pop_up_window():
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


class medical_entry_window():
    def __init__(self, master, conn, main_win):
        self.conn = conn
        self.master = master
        self.med_dict = {}          # dictionary of button ID's and animal ids
        self.master.withdraw()      # Hide window
        self.master.wm_title("Medical Entries")
        self.master.geometry("1024x700")
        self.main_win = main_win    # Used for comunicating with parent window.
        self._build_frames()
        self._build_widgets()
        self.master.deiconify()     # show window
        self.popup = 'not created'  # Check used later to see if popup created.

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
        self.left_frame = ttk.Frame(self.master, style="pink.TFrame")
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
        md = basic_db_query(self.conn, animal_query)
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
        text = "| Next Vac Due : "
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
                    value_dict['Due_Date'] = due_date

            # If Other
            elif combo == "Other":
                value_dict['Medical_Type'] = combo
                
                # Add Cost
                cost = getattr(self, "medcoste" + ids).get()
                value_dict['Cost'] = float(cost)
                
                # Check other-type box
                othertype = getattr(self, "medotheropl" + ids)
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
            sqlstr = sqlstr[:len(sqlstr) - 2]   # remove final command and newline

            sqlstr += ')\nVALUES (\n'

            # Adding value headings.
            for k, v in value_dict.items():
                sqlstr += ':' + str(k) + ',\n'
            sqlstr = sqlstr[:len(sqlstr) - 2]   # remove final command and newline

            sqlstr += ')'
            print(sqlstr)
            print(value_dict)
            adv_db_query(self.conn, sqlstr, value_dict, returnlist=False)

    def close_window(self):
        self.master.destroy()

    def refresh_animal_data(self):
        md_query = "SELECT * FROM Animal_ID_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = basic_db_query(self.conn, md_query)
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
                othertype = getattr(self, "medotheropl" + ids)
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
        if self.popup == 'not created':
            self.popup = pop_up_window(tk.Toplevel(self.master),
                                       heading=heading,
                                       text=text,
                                       main_win=self)
            self.popup.text_box.lift()
            self.popup.text_box.focus_force()
        else:
            self.popup.replace_text(text=text)
            self.popup.text_box.lift()
            self.popup.text_box.focus_force()


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
