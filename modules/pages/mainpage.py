"""
Front page for the rescue:

The front page has multiple tabs:
Tab 1: Dashboard
- Shows all animals currently in the rescue (searchable, filterable, sortable)
- Buttons to add new animals and medcial events.
"""
import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk
import configparser
from PIL import Image, ImageTk
from modules.othermodules.sqlitefunctions import BasicDbQuery
from modules.othermodules.treebuild import TreeBuild
from modules.pages.medicalpage import MedicalEntryWindow
from modules.pages.animalpage import AnimalWindow
from modules.pages.homingpage import HomingWindow
from modules.othermodules.tk_window import CenterWindow
from modules.othermodules.medicalpopup import medical_popup
from modules.othermodules.filesandfolders import (
    check_rel_folder, get_full_path, copy_files, check_rel_file,
    file_extension)
from tkinter.filedialog import askopenfilenames

class BuildMainWindow():
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
        self._setup_tab_2_frames()
        self._setup_tab_2_widgets()
        self._setup_tab_3_frames()
        self._setup_tab_3_widgets()

    def _setup_window(self):
        # Get and read config
        self.config = configparser.ConfigParser()
        self.config.read('Config/config.ini')

        # Set window title to name from config
        self.title = self.config['DEFAULT'].get('rescuename',
                                                'Rescue name not set up yet')
        wm_title = self.title
        self.master.wm_title(wm_title)

        CenterWindow(self.master)

    def _setup_fonts(self):
        # Title Font settings
        self.font_title = tkfont.Font(size=30, weight='bold')

        # Sub-headings labels
        self.font_sub_title = tkfont.Font(size=18)

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
        self.tab2 = ttk.Frame(note)
        self.tab3 = ttk.Frame(note)

        # Asign the above frames to tabs
        note.add(self.tab1, text="  Dashboard  ")
        note.add(self.tab2, text="  Medical History  ")
        note.add(self.tab3, text="  Homing History  ")

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

        # Add new homing event button
        homing_button = ttk.Button(
            self.buttons_frame,
            text="Home a " + animal_type,
            command=self.open_homing_window)
        homing_button.pack(side="left", anchor="nw", padx=6)

        # Import images button
        import_img_button = ttk.Button(
            self.buttons_frame,
            text="Import Images",
            command=self._add_images)
        import_img_button.pack(side="left", anchor="nw", padx=6)

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
        md = BasicDbQuery(self.conn, md_query)
        self.main_tree = TreeBuild(self.tree_search_frame,
                                   search=True,
                                   data=md[1],
                                   # widths=main_search_widths,
                                   headings=md[0])
        self.main_tree.tree.bind(
            "<Double-1>",
            lambda c: self.open_animal_window(
                self.main_tree.tree.item(self.main_tree.tree.focus()), c))

    def _setup_tab_2_frames(self):      # Medical history
        # Header Frame
        self.med_header = ttk.Frame(self.tab2)
        self.med_header.pack(side="top", fill="x")

        # Medical history frame
        self.med_tree_frame = ttk.Frame(self.tab2)
        self.med_tree_frame.pack(side="top", fill="both", expand=True)

    def _setup_tab_2_widgets(self):     # Medical history
        # Title
        med_title = ttk.Label(self.med_header, text="Medical History")
        med_title['font'] = self.font_title
        med_title.pack(side="top", anchor="n")

        # Medical History Tree
        # Get data
        sql_query = "SELECT * FROM Main_Page_Med_History"
        med_results = BasicDbQuery(self.conn, sql_query)
        med_tree = TreeBuild(self.med_tree_frame,
                             search=True,
                             widths=[40, 60, 120, 80, 50, 2000],
                             data=med_results[1],
                             headings=med_results[0])
        med_tree.tree.bind(
            "<Double-1>",
            lambda c: medical_popup(self, med_tree.tree, c))

    def _setup_tab_3_frames(self):      # Homing History
        # Header Frame
        self.homing_header = ttk.Frame(self.tab3)
        self.homing_header.pack(side="top", fill="x")

        # Medical history frame
        self.homing_tree_frame = ttk.Frame(self.tab3)
        self.homing_tree_frame.pack(side="top", fill="both", expand=True)

    def _setup_tab_3_widgets(self):     # Homing History
        # Title
        homing_title = ttk.Label(self.homing_header, text="Homing History")
        homing_title['font'] = self.font_title
        homing_title.pack(side="top", anchor="n")

        # Medical History Tree
        # Get data
        sql_query = "SELECT * FROM Main_Page_Homing_History"
        homing_results = BasicDbQuery(self.conn, sql_query)
        homing_tree = TreeBuild(self.homing_tree_frame,
                                search=True,
                                widths=[70, 40, 100, 95, 120, 300, 100, 2000],
                                data=homing_results[1],
                                headings=homing_results[0])
        # Needed to stop linter from moaning about being un-used
        # It will be used at a later date
        homing_tree

    def refresh_main_tree(self):
        md_query = "SELECT * FROM Main_Page_View"
        if self.in_rescue_var.get() == 1:
            md_query += "_Active"
        md = BasicDbQuery(self.conn, md_query)
        self.main_tree.refresh_data(md[1])

    def add_new_animal_window(self):
        AnimalWindow(tk.Toplevel(self.master), self.conn, self,
                     window_type="new")

    def open_medical_entry_window(self):
        self.med_win = MedicalEntryWindow(tk.Toplevel(self.master),
                                          self.conn, self)

    def open_homing_window(self):
        self.homing_win = HomingWindow(tk.Toplevel(self.master),
                                       self.conn, self)

    def open_animal_window(self, row_selected, event=None):
        region = self.main_tree.tree.identify("region", event.x, event.y)
        if region != "heading":
            animal_id = row_selected['values'][0]
            AnimalWindow(tk.Toplevel(self.master), self.conn, self,
                         window_type="edit", animal_id=animal_id)

    def _add_images(self):
        # Check folder exists and create if needed
        rel_folder = 'images\\untagged\\'
        check_rel_folder(rel_folder, create=True)

        # Ask user to pick photos:
        img_list = askopenfilenames(filetypes=[(
            "Images", "*.jpg *.jpeg *.png")])

        for img in img_list:
            # get next available file name
            fileexist = True
            img_num = 0
            img_extension = file_extension(img)
            while fileexist:
                img_name = 'IMG_' + str(img_num)
                rel_file = rel_folder + img_name + img_extension
                if check_rel_file(rel_file):
                    img_num += 1
                else:
                    fileexist = False

            # Copy over file
            new_path = get_full_path(rel_file)
            copy_files(img, new_path)

        msgbox = tk.messagebox.askquestion(
            'Tag Photos?',
            "Do you want to tag the photo's now?")
        if msgbox == 'yes':
            self.open_tag_photo_window(self)