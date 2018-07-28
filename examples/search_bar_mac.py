# Translated from Tcl code by Schelte Bron, http://wiki.tcl.tk/18188
# Found at https://gist.github.com/rhoit/6342234

from tkinter import *
import tkinter.ttk as ttk


magnifying_glass_icon = "pic.dat"


class SearchStyle():
    def __init__(self,):
        self.entrystyle()
        self._entry = None

    @property
    def _entry(self):
        return self._entry

    def create_entry(self, parent, width):
        self._entry = ttk.Entry(parent, style="Search.entry", width=width)
        return self._entry

    def entrystyle(self):
        data = open("pic.dat").read()
        global s1, s2
        s1 = PhotoImage("search1", data=data, format="gif -index 0")
        s2 = PhotoImage("search2", data=data, format="gif -index 1")
        style = ttk.Style()
        style.element_create("Search.field", "image", "search1",
            ("focus", "search2"), border=[22, 7, 14], sticky="ew")
        style.layout("Search.entry", [
            ("Search.field", {"sticky": "nswe", "border": 1, "children":
                [("Entry.padding", {"sticky": "nswe", "children":
                    [("Entry.textarea", {"sticky": "nswe"})]
                })]
            })]
        )
        style.configure("Search.entry", background="#b2b2b2")

class SearchBar(Frame):
    def __init__(self, parent):

        Frame.__init__(parent)

        button = Button(parent,)

if __name__ == '__main__':
    root = Tk()
    root.configure(background="#b2b2b2")
    e1 = SearchStyle()
    e1 = e1.create_entry(root, 20)
    # e1 = ttk.Entry(root, style="Search.entry", width=20)
    e1.pack()
root.mainloop()