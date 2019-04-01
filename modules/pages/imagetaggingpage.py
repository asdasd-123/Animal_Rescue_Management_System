"""
Image Tagging Page:

Used to asign photo's to specified animals.
When asignment is made, pull across and rename photo's to avoid overlap,
and store asignments in DB
"""
from modules.othermodules.tk_window import CenterWindow
from modules.othermodules.treebuild import TreeBuild
from modules.othermodules.sqlitefunctions import BasicDbQuery
from modules.othermodules.filesandfolders import (
    get_rel_file_list, get_full_path, file_extension)
from modules.othermodules.globals import Globals
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from os import startfile
from os import remove as remove_file
import subprocess


class ImageTaggingWindow():
    def __init__(self, master, conn, main_win):
        # Init variable setup
        self.master = master
        self.conn = conn
        self.main_win = main_win
        self.current_file = 0
        self.animal_dict = {}       # Dictionary of row IDs and animal ID's
        #                             for adding animals to the list.

        # Window setup
        self.master.wm_title("Image Tagging")
        CenterWindow(self.master)

        # Build window
        self._build_frames()
        self._build_widgets()

        # Get list of images
        self.file_list = get_rel_file_list('images\\untagged\\',
                                           return_type='paths')
        # Load first image
        self._load_image(0)

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
        self.photo_frame = ttk.Label(self.image_holder)
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
        previous_button = ttk.Button(
            self.photo_buttons_frame,
            text="<-----",
            command=lambda: self._load_image(self.current_file - 1),
            style="img.TButton")
        previous_button.pack_propagate(0)
        previous_button.pack(side="left", fill="both", expand="true",
                             padx=10, pady=10)
        tag_photo = ttk.Button(self.photo_buttons_frame,
                               text="Tag", style="img.TButton")
        tag_photo.pack_propagate(0)
        tag_photo.pack(side="left", fill="both", expand="true",
                       padx=10, pady=10)
        del_photo = ttk.Button(self.photo_buttons_frame,
                               text="Delete",
                               command=lambda: self._delete_file(),
                               style="img.TButton")
        del_photo.pack_propagate(0)
        del_photo.pack(side="left", fill="both", expand="true",
                       padx=10, pady=10)
        open_photo = ttk.Button(self.photo_buttons_frame,
                                text="Open",
                                command=lambda: self.open_file(),
                                style="img.TButton")
        open_photo.pack_propagate(0)
        open_photo.pack(side="left", fill="both", expand="true",
                        padx=10, pady=10)
        next_button = ttk.Button(
            self.photo_buttons_frame,
            text="----->",
            command=lambda: self._load_image(self.current_file + 1),
            style="img.TButton")
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

    def _load_image(self, num):
        self.current_file = num
        # Check if any images are present first.
        if len(self.file_list) == 0:
            tk.messagebox.showinfo('', 'There are no files to Tag')
            self.master.destroy()
            return

        # Check if requested file it outside of range
        if num < 0:
            next_file_num = (len(self.file_list) - 1)
            self._load_image(next_file_num)
            return
        elif num > len(self.file_list) - 1:
            next_file_num = 0
            self._load_image(next_file_num)
            return

        # To keep track of current photo when deleting/tagging
        current_img = self.file_list[num]

        # Get frame width and height.
        self.photo_frame.update()
        w = self.photo_frame.winfo_width()
        h = self.photo_frame.winfo_height()

        # ============
        # Check if image or video or other.
        # And load image accordingly
        # ============
        extension = file_extension(current_img).upper()
        if extension in ('.JPG', '.JPEG', '.PNG'):
            self.file_type = 'Image'
            thumbnail_im = Image.open(current_img)
        elif extension in ('.AVI', '.MP4', '.FLV', '.MP4', '.MPEG'):
            self.file_type = 'Video'
            thumbnail_im = Image.open('images\\defaults\\Video.png')
        else:
            self.file_type = 'Unknown'
            thumbnail_im = Image.open('images\\defaults\\Unknown.png')

        # =============
        # Resize image to 300px in largest dimension
        # =============
        # Get new width and height
        old_w = thumbnail_im.width
        old_h = thumbnail_im.height
        dimension = (old_w, old_h)

        if old_w > w or old_h > h:
            # Check if it needs resizing
            if old_w <= old_h:
                max_dimension = h
                nw = int(round(old_w / old_h * max_dimension, 0))
                nh = max_dimension
            else:
                max_dimension = w
                nh = int(round(old_h / old_w * max_dimension, 0))
                nw = max_dimension
            dimension = (nw, nh)

        # Update image on page
        thumbnail_im = thumbnail_im.resize(dimension, Image.ANTIALIAS)
        thumbnail_ph = ImageTk.PhotoImage(thumbnail_im)
        self.photo_frame.configure(image=thumbnail_ph)
        self.photo_frame.image = thumbnail_ph
        self.photo_frame.update()   # Seems to make it a bit 'snappier'

    def open_file(self):
        """Opens current file from the viewer"""
        path = get_full_path(self.file_list[self.current_file])
        if self.file_type in ('Image', 'Video'):
            startfile(path)
        else:
            path_string = 'explorer /select,"' + path + '"'
            subprocess.Popen(path_string)

    def _delete_file(self):
        """Deletes the current file from the unsorted folder"""
        # Need to temporarily hide root window else it changes focus
        # when asking for file name.
        Globals.root.withdraw()

        # Ask if user wants to delete the file
        msgbox = tk.messagebox.askquestion(
            'Confirmation',
            'Are you sure you want to delete this file?')

        # Bring animal window to front again and unhide root window
        Globals.root.deiconify()
        self.photo_frame.lift()
        self.photo_frame.focus_force()

        # If yes, remove file and pop from file list.
        if msgbox == 'yes':
            path = get_full_path(self.file_list[self.current_file])
            remove_file(path)
            self.file_list.remove(self.file_list[self.current_file])
            self._load_image(self.current_file - 1)
