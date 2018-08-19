"""The tkinter frame containing the search box, button, and results table"""

import sys

from view.search.result_table import ResultTable
from view.search.search_box import SearchBox

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
    from tkinter.constants import *


class SearchFrame(Tk.Frame):
    def __init__(self, parent, event_handler, controller):
        Tk.Frame.__init__(self, parent)
        self._event_handler = event_handler
        self.controller = controller

        # Create gui components and pack them
        search_box = SearchBox(self, command=self.on_search, placeholder="Type and press enter",
                               entry_highlightthickness=0)
        search_box.pack(pady=6, padx=3, side=TOP, fill=X)

        self.table = ResultTable(self)
        self.table.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

    @property
    def event_handler(self):
        return self._event_handler

    def on_search(self, text):
        """
        Retrieves text entered in the textbox
        :param text: Text inputted in the search entry field
        :return:
        """
        timestamps = self.controller.get_timestamps(text)
        self.table.update_results(timestamps)
