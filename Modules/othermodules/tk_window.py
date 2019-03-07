"""
For functions I use regularly to interact with tkinter windows.
"""
import configparser


def CenterWindow(window):
    config = configparser.ConfigParser()
    config.read('Config/config.ini')

    width = int(config['DEFAULT'].get('windowwidth'))
    height = int(config['DEFAULT'].get('windowheight'))

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # work  out coords
    y = (screen_height/2) - (height/2)
    x = (screen_width/2) - (width/2)

    window.geometry('%dx%d+%d+%d' % (width, height, x, y - 40))
