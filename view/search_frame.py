import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.messagebox import showinfo
    from tkinter.constants import *

from view.search_box import SearchBox


class SearchFrame(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)

        search_box = SearchBox(self, command=self.on_search, placeholder="Type and press enter", entry_highlightthickness=0)
        search_box.pack(pady=6,padx=3, side=TOP, fill=X)

    def on_search(self, text):
        """
        Retrieves text entered in the textbox
        :param text: Text inputted in the search entry field
        :return:
        """
        showinfo(text)
