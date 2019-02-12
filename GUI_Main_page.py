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


class build_main_window():
    """Builds the main window"""
    def __init__(self, master, conn):
        self.master = master
        self.conn = conn
        self._Setup_window()
        self._Setup_fonts()
        self._Setup_styles()
        self._Setup_tabs()      # Setting up tabs (notebook) widget
        self._Setup_tab_1()     # Setting up tab1 (Dashboard) widgets

    def _Setup_window(self):
        # Get and read config
        config = configparser.ConfigParser()
        config.read('Config/config.ini')

        # Set window title to name from config
        self.window_title = config['DEFAULT'].get('rescuename',
                                                  'Rescue name not set up yet')
        wm_title = self.window_title
        self.master.wm_title(wm_title)

        # Set window size on launch
        self.master.geometry("1024x768")

    def _Setup_fonts(self):
        # Title Font settings
        self.font_title = tkfont.Font(size=30, weight='bold')

        # Search box font
        self.font_search = tkfont.Font(size=12)

    def _Setup_styles(self):
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

    def _Setup_tabs(self):
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

    def _Setup_tab_1(self):
        # Header Frame. Contains Title, Logo, and tree-filters
        header = ttk.Frame(self.tab1)
        header.pack(side="top", fill="x")

        # - Logo Frame. Contains the logo picture
        logo_frame = ttk.Frame(header, width="150", height="160")
        logo_frame.pack_propagate(0)
        logo_frame.pack(side="right")

        # -- Load logo and create label for it
        logo_im = Image.open("catlogo.png")
        logo_ph = ImageTk.PhotoImage(logo_im)
        logo_img = ttk.Label(logo_frame, image=logo_ph)
        logo_img.image = logo_ph
        logo_img.pack(side="top")

        # - Header/Filter Frame
        header_filter = ttk.Frame(header, padding="10")
        header_filter.pack(side="left", expand=True, fill="both")

        # -- Title Label
        title = ttk.Label(header_filter, text=self.window_title)
        title['font'] = self.font_title
        title.pack(side="top", anchor="w")

        # -- Filters LabelFrame
        filters = ttk.LabelFrame(header_filter, text="Filters")
        filters.pack(side="bottom", anchor="sw", expand=True, fill="both")

        # Tree/Search Frame
        tree_search_frame = ttk.Frame(self.tab1)
        tree_search_frame.pack(expand=True, fill="both")

        # Get tree data and build tree (main data=md)
        md_query = "SELECT * FROM Main_Page_View"
        md = basic_db_query(self.conn, md_query)
        main_tree = TreeBuild(tree_search_frame,
                              search=True,
                              data=md[1],
                              # widths=main_search_widths,
                              headings=md[0])
        main_tree.tree.bind(
            "<Double-1>",
            lambda c: self.open_animal_window(
                main_tree.tree.item(main_tree.tree.focus())))

    def open_animal_window(self, row_selected):
        animal_id = row_selected['values'][0]
        animal_window(tk.Toplevel(self.master), self.conn, animal_id)


class animal_window():
    def __init__(self, master, conn, animal_id=""):
        self.conn = conn
        self.master = master
        self.master.geometry("1680x900")
        self.animal_id = animal_id
        self._Setup_fonts()
        self._build_frames()
        self._build_widgets()
        print("Building animal window")

    def _Setup_fonts(self):
        # Title Font settings
        self.font_title = tkfont.Font(size=30, weight='bold')

    def _build_frames(self):
        # Right Frame
        self.right_frame = ttk.Frame(self.master, width="300", style="green.TFrame")
        self.right_frame.pack(side="right", fill="both")

        # - Image frame
        self.image_frame = ttk.Frame(self.right_frame, width="300", height="300", style="yellow.TFrame")
        self.image_frame.pack(side="top", fill="x")

        # Left frame
        self.left_frame = ttk.Frame(self.master, style="blue.TFrame")
        self.left_frame.pack(side="left", expand=True, fill="both")

        # - Title frame
        self.title_frame = ttk.Frame(self.left_frame, style="grey.TFrame")
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

        # - Central frame
        self.central_frame = ttk.Frame(self.left_frame, style="brown.TFrame")
        self.central_frame.pack(side="top", fill="both", expand=True)

    def _build_widgets(self):
        # - Title Label
        self.title = ttk.Label(
            self.title_frame,
            text=self.animal_id,
            font=self.font_title)
        self.title.pack(side="top", fill="x")

        # - Column 0 items
        # - DOB known
        self.dob_known_0 = ttk.Label(self.data_col[0][0], text="DOB known?: ", anchor="w")
        self.dob_known_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.dob_known_1 = ttk.Combobox(self.data_col[0][1], state='readonly', values=('N', 'Y'))
        self.dob_known_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Date of birth
        self.dob_0 = ttk.Label(self.data_col[0][0], text="Date of Birth (DD/MM/YYYY): ")
        self.dob_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.dob_1 = ttk.Entry(self.data_col[0][1], text="25 Jan 2018")
        self.dob_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Colour
        self.colour_0 = ttk.Label(self.data_col[0][0], text="Colour: ")
        self.colour_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.colour_1 = ttk.Entry(self.data_col[0][1], text="temp")
        self.colour_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Sex
        self.sex_0 = ttk.Label(self.data_col[0][0], text="Sex: ", anchor="w")
        self.sex_0.pack(side="top", anchor="w", ipady=self.col_paddl)
        self.sex_1 = ttk.Combobox(self.data_col[0][1], state='readonly', values=('UNKNOWN', 'M', 'F'))
        self.sex_1.pack(side="top", anchor="w", pady=self.col_padd)

        # - Column 0 items
        # - Chip Number
        self.chip_num_0 = ttk.Label(self.data_col[1][0], text="Chip Number: ")
        self.chip_num_0.pack(side="top", anchor="w", ipady=self.col_padd)
        self.chip_num_1 = ttk.Entry(self.data_col[1][1], text="temp")
        self.chip_num_1.pack(side="top", anchor="w", pady=self.col_padd)


def basic_db_query(conn, query):  # (sqlmd gonig forward)
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

# def display_animal_window():
#     root_a.mainloop()
