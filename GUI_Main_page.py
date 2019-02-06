"""
Builds the main page of the rescue screen
"""
# Imports
import tkinter
import tkinter.font
import tkinter.ttk as ttk
import configparser
from PIL import Image, ImageTk

root = tkinter.Tk()

# Remove this after database is setup.
# For testing purposes only at the moment.
main_search_headings = ["ID", "Name", "Chip No. ", "Vaccinated"]
main_search_data = [
    ("1", "Cookie", "7493732", "42005"),
    ("2", "Gibbie", "7342152", "42038"),
    ("3", "Tinkerbelle", "1681023", "42071"),
    ("4", "Wispa", "6369268", "42104"),
    ("5", "Pebbles", "4362464", "42137"),
    ("6", "Tatsiana", "5674374", "42170"),
    ("7", "Cookiea", "9076052", "42203"),
    ("8", "Gibbiea", "6237524", "42236"),
    ("9", "Tinkerbellea", "6159266", "42269"),
    ("10", "Wispaa", "1521653", "42302"),
    ("11", "Pebblesa", "8150588", "42335"),
    ("12", "Tatsianaa", "1505322", "42368"),
    ("13", "Cookieaa", "4445858", "42401"),
    ("14", "Gibbieaa", "6390976", "42434"),
    ("15", "Tinkerbelleaa", "1968907", "42467"),
    ("16", "Wispaaa", "1501928", "42500"),
    ("17", "Pebblesaa", "3430556", "42533"),
    ("18", "Tatsianaaa", "6453150", "42566"),
    ("19", "Cookieaaa", "3750061", "42599"),
    ("20", "Gibbieaaa", "1742287", "42632"),
    ("21", "Tinkerbelleaaa", "7138771", "42665"),
    ("22", "Wispaaaa", "4020316", "42698"),
    ("23", "Pebblesaaa", "6514509", "42731"),
    ("24", "Tatsianaaaa", "1438670", "42764"),
    ("25", "Cookieaaaa", "1151414", "42797"),
    ("26", "Gibbieaaaa", "8535522", "42830"),
    ("27", "Tinkerbelleaaaa", "4106620", "42863"),
    ("28", "Wispaaaaa", "4390267", "42896"),
    ("29", "Pebblesaaaa", "2554880", "42929"),
    ("30", "Tatsianaaaaa", "7180502", "42962"),
    ("31", "Cookieaaaaa", "9735914", "42995")
    ]


class Build_main_window(object):
    """Builds the main window"""
    def __init__(self):
        self._Setup_window()
        self._Setup_fonts()
        self._Setup_styles()
        self._Setup_tabs()      # Setting up tabs (notebook) widget
        self._Setup_tab_1()     # Setting up tab1 (Dashboard) widgets

    def _Setup_fonts(self):
        # Title Font settings
        self.font_title = tkinter.font.Font(size=30, weight='bold')

        # Search box font
        self.font_search = tkinter.font.Font(size=15)

    def _Setup_window(self):
        # Get and read config
        config = configparser.ConfigParser()
        config.read('Config/config.ini')

        # Set window title to name from config
        self.window_title = config['DEFAULT'].get('rescuename',
                                                  'Rescue name not set up yet')
        root_wm_title = self.window_title
        root.wm_title(root_wm_title)

        # Set window size on launch
        root.geometry("1024x768")

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
        note = ttk.Notebook(root)

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
        tree_search_frame = ttk.Frame(self.tab1, style="blue.TFrame")
        tree_search_frame.pack(expand=True, fill="both")

        # - Search Frame
        search_frame = ttk.Frame(tree_search_frame, style="yellow.TFrame")
        search_frame.pack(side="top", fill="x")

        # -- Filling the search Frame with search boxes
        # -- ID search box
        search_id_frame = ttk.Frame(search_frame,
                                    width="100",
                                    height="40",
                                    padding="5")
        search_id_frame.pack_propagate(0)
        search_id_frame.pack(side="left")
        search_id = ttk.Entry(search_id_frame, exportselection=0)
        search_id['font'] = self.font_search
        search_id.pack(side="left", expand=True, fill="both")

        # -- Name search box
        search_name_frame = ttk.Frame(search_frame,
                                      width="120",
                                      height="40",
                                      padding="5")
        search_name_frame.pack_propagate(0)
        search_name_frame.pack(side="left")
        search_name = ttk.Entry(search_name_frame, exportselection=0)
        search_name['font'] = self.font_search
        search_name.pack(side="left", expand=True, fill="both")

        # -- Chip Number search box
        search_chipno_frame = ttk.Frame(search_frame,
                                        width="220",
                                        height="40",
                                        padding="5")
        search_chipno_frame.pack_propagate(0)
        search_chipno_frame.pack(side="left")
        search_chipno = ttk.Entry(search_chipno_frame, exportselection=0)
        search_chipno['font'] = self.font_search
        search_chipno.pack(side="left", expand=True, fill="both")

        # -- Vaccinated search box
        search_vaccinate_frame = ttk.Frame(search_frame,
                                           width="120",
                                           height="40",
                                           padding="5")
        search_vaccinate_frame.pack_propagate(0)
        search_vaccinate_frame.pack(side="left")
        search_vaccinate = ttk.Entry(search_vaccinate_frame, exportselection=0)
        search_vaccinate['font'] = self.font_search
        search_vaccinate.pack(side="left", expand=True, fill="both")


def Display_main_window():
    root.mainloop()
