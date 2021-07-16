import os
import tkinter as tk


class Application(tk.Tk):
    def __init__(self):
        if not os.environ.get('DISPLAY', '') == '':
            tk.Tk.__init__(self)
