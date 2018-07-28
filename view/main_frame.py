import os
import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Frame, Label, Button

from view.video_frame import VideoFrame


class MainFrame(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)

        self.root = tk.Frame(self, width=800, height=600)
        self.root.pack(side="top", fill="both", expand=True)
        self.winfo_toplevel().title("TITLE")
        self.protocol("WM_DELETE_WINDOW", self._quit)
        leftFrame = Frame(self.root)
        rightFrame = Frame(self.root)

        leftFrame.pack(side=LEFT)
        rightFrame.pack(side=RIGHT)

        self.generate_browse_and_search(rightFrame)
        self.generate_video(rightFrame)

    def _quit(self):
        print("_quit: bye")
        self.quit()  # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        os._exit(1)

    def generate_browse_and_search(self, parent):
        sub_frame = Frame(parent)
        sub_frame.pack(fill=X)
        browse_bttn = Button(sub_frame, text="Browse",command=self.on_dummy)
        browse_bttn.grid(row=0, column=0)

        path_label = Label(sub_frame, text="BLANK")
        path_label.grid(row=0,column=1)

    def generate_video(self, parent):
        video = VideoFrame(parent)
        video.pack()
        video.pack(fill=X)


    def on_dummy(self):
        print("Clicked on something")

view = MainFrame()
view.mainloop()