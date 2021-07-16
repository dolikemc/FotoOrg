import tkinter as tk
import os


class Application(tk.Tk):
    def __init__(self):
        if os.environ.get('DISPLAY', '') == '':
            os.environ['DISPLAY'] = ':0'
        tk.Tk.__init__(self)
