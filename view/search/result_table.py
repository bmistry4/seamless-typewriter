import sys
from view.search.constants import TABLE_HEADINGS
if sys.version_info[0] < 3:
    from tkinter import ttk
else:
    from tkinter import ttk
    from tkinter.constants import *
    import tkinter.font as tkfont

# List of column heading names
COLUMN_HEADINGS = [constant.value[0] for constant in TABLE_HEADINGS]
data = [(i, i * 123234) for i in range(20)]


class ResultTable(ttk.Frame):
    """
    Represents the GUI frame for the table containing the search results
    """

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.tree = ttk.Treeview(columns=COLUMN_HEADINGS, show="headings")

        self.add_scrollbars()
        self.create_tree()

        # Event bindings
        self.tree.bind("<Double-1>", self.on_double_click)

    def add_scrollbars(self):
        """
        Adds vertical and horizontal scrolling to the table

        :return: None
        """
        vsb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky=NSEW, in_=self)
        vsb.grid(column=1, row=0, sticky=NS, in_=self)
        hsb.grid(column=0, row=1, sticky=EW, in_=self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def on_double_click(self, event):
        """
        when a row in the table is double clicked, set the video slider to the selected second

        :param event: event launched from double click
        :return: none
        """
        # get selected row
        item = self.tree.identify('item', event.x, event.y)
        values = self.tree.item(item)["values"]
        # Get the column index for time (i.e. 0)
        time_col_index = TABLE_HEADINGS.get_index(TABLE_HEADINGS.TIME.value)
        # Calculate the timestamp for the index
        ts_sec = values[time_col_index]
        ts_ms = self.sec_to_ms(ts_sec)
        # Set video player time
        self.parent.event_handler.timeslider_last_val = ("%.0f" % ts_sec) + ".0"
        self.parent.event_handler._time_slider.set(ts_sec)
        # Set slider time
        self.parent._event_handler._player.set_time(int(ts_ms))

    def sec_to_ms(self, val):
        """
        Convert seconds to milliseconds
        :param val: time in seconds
        :return: time in milliseconds
        """
        # 1000 ms in 1 ms
        return val * 1000

    def create_tree(self):
        """
        Creates the table and populates it
        :return:
        """
        for col in COLUMN_HEADINGS:
            # adjust the column's width to the header string
            self.tree.column(col, width=tkfont.Font().measure(col.title()))

        self._insert_data(data)

    def _insert_data(self, data):
        """
        Add rows to the table
        :param data: List of tuples which represent the rows
        :return: None
        """
        for item in data:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for col_index, val in enumerate(item):
                col_w = tkfont.Font().measure(val)
                if self.tree.column(COLUMN_HEADINGS[col_index], width=None) < col_w:
                    self.tree.column(COLUMN_HEADINGS[col_index], width=col_w)

    def update_results(self, results):
        """
        Clear the current tree and update it with the new results
        :param results: List of tuples containing row information
        :return: None
        """
        self.tree.delete(*self.tree.get_children())
        if results is not None:
            self._insert_data(results)
        else:
            self._insert_data([("No results found", )])

