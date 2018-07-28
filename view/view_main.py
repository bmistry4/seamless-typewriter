import tkinter as Tk
from view.main_frame import MainFrame
import os


class ViewMain:
    def __init__(self):
        # Create a Tk.App(), which handles the windowing system event loop
        self.root = self.Tk_get_root()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.winfo_toplevel().title("TITLE")
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

        MainFrame(self.root)

        # show the player window centred and run the application
        self.root.mainloop()

    def Tk_get_root(self):
        if not hasattr(self, "root"):  # (1)
            self.root = Tk.Tk()  # initialization call is inside the function
        return self.root

    def _quit(self):
        print("_quit: bye")
        root = self.Tk_get_root()
        root.quit()  # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        os._exit(1)


ViewMain()
