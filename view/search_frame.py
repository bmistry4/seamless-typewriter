"""The tkinter frame containing the search box, button, and results table"""

import sys
from view.search_box import SearchBox
from view.result_table import ResultTable

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
    from tkinter.messagebox import showinfo
    from tkinter.constants import *


class SearchFrame(Tk.Frame):
    def __init__(self, parent, event_handler):
        Tk.Frame.__init__(self, parent)
        self._event_handler = event_handler

        search_box = SearchBox(self, command=self.on_search, placeholder="Type and press enter",
                               entry_highlightthickness=0)
        search_box.pack(pady=6, padx=3, side=TOP, fill=X)

        table = ResultTable(self)
        table.pack(fill=BOTH, expand=True)
        # frame = Tk.Frame(self, height=400)
        # frame.configure(background='blue')
        # frame.pack(fill=X)

    @property
    def event_handler(self):
        return self._event_handler

    def on_search(self, text):
        """
        Retrieves text entered in the textbox
        :param text: Text inputted in the search entry field
        :return:
        """
        showinfo("Inputted", text)
