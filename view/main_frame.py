import tkinter as Tk
from tkinter.constants import *
from tkinter.ttk import Frame, Label, Button

from view.video_frame import VideoFrame
from view.video_events import Events
from view.search_frame import SearchFrame

class MainFrame(Frame):
    def __init__(self, root_Tk, width=800, height=600):
        self.root_Tk = root_Tk

        Frame.__init__(self, root_Tk, width=width, height=height)

        self.event_handler = Events(self)
        self.pack(side=TOP, fill=BOTH, expand=True)

        self.status = Label(self, text="Video:", relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)


        leftFrame = Frame(self)
        rightFrame = Frame(self)

        leftFrame.pack(side=LEFT)
        rightFrame.pack(side=RIGHT)

        search_panel = SearchFrame(leftFrame)
        search_panel.pack()

        self.generate_menubar(root_Tk)
        # self.generate_browse_and_search(rightFrame)
        self.generate_video(rightFrame)


    def generate_menubar(self, parent):
        menubar = Tk.Menu(parent)
        parent.config(menu=menubar)

        file_menu = Tk.Menu(menubar)
        file_menu.add_command(label="Open", underline=0, command=self.event_handler.on_open)
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

    def update_status_bar(self, text):
        """
        Updates the status bar on main frame

        :param
            text: New text for status bar
        :return:
            None
        """
        self.status['text'] = text

    def on_dummy(self):
        print("Clicked on something")
