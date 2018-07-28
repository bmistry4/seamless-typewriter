import os
import tkinter as Tk
from tkinter.constants import *
from tkinter.ttk import Frame, Label, Button

from view.video_frame import VideoFrame
from view.video_events import Events


class MainFrame(Frame):
    def __init__(self, root_Tk):
        self.root_Tk = root_Tk

        Frame.__init__(self, root_Tk, width=800, height=600)

        self.event_handler = Events(self)
        self.pack(side="top", fill="both", expand=True)
        leftFrame = Frame(self)
        rightFrame = Frame(self)

        leftFrame.pack(side=LEFT)
        rightFrame.pack(side=RIGHT)

        self.generate_menubar(root_Tk)
        self.generate_browse_and_search(rightFrame)
        self.generate_video(rightFrame)

    def generate_menubar(self, parent):
        menubar = Tk.Menu(parent)
        parent.config(menu=menubar)

        file_menu = Tk.Menu(menubar)
        file_menu.add_command(label="Open", underline=0, command=self.event_handler.OnOpen)
        menubar.add_cascade(label="File", menu=file_menu)

    def generate_browse_and_search(self, parent):
        sub_frame = Frame(parent)
        sub_frame.pack(fill=X)
        browse_bttn = Button(sub_frame, text="Browse",command=self.on_dummy)
        browse_bttn.grid(row=0, column=0)

        path_label = Label(sub_frame, text="BLANK")
        path_label.grid(row=0,column=1)

    def generate_video(self, parent):
        video = VideoFrame(parent, self.event_handler)
        video.pack()
        video.pack(fill=X)

    def on_dummy(self):
        print("Clicked on something")
