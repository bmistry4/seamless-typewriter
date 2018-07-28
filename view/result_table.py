import sys
import time
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.messagebox import showinfo
    from tkinter.constants import *
    import tkinter.font as tkFont

COLUMN_HEADINGS = ["Time", "Text"]
data = [(i, i * 123234) for i in range(20)]


class ResultTable(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.tree = ttk.Treeview(columns=COLUMN_HEADINGS, show="headings")
        vsb = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky=NSEW, in_=self)
        vsb.grid(column=1, row=0, sticky=NS, in_=self)
        hsb.grid(column=0, row=1, sticky='ew', in_=self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_tree()
        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        values = self.tree.item(item)["values"]
        print(values)
        # return index only
        # TODO - make so not index (general)
        ts_sec = values[0]
        ts_ms = self.sec_to_ms(ts_sec)
        print(ts_sec)
        # Set video player time
        self.master._event_handler.timeslider_last_val = ("%.0f" % ts_sec) + ".0"
        self.master._event_handler._time_slider.set(ts_sec)
        # Set slider time
        self.master._event_handler._player.set_time(int(ts_ms))

    def sec_to_ms(self, val):
        # 1000 ms in 1 ms
        return val*1000

    def create_tree(self):
        for col in COLUMN_HEADINGS:
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()))

        for item in data:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for col_index, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(COLUMN_HEADINGS[col_index], width=None) < col_w:
                    self.tree.column(COLUMN_HEADINGS[col_index], width=col_w)
