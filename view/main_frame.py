import tkinter as tk
from tkinter.constants import *
from tkinter.ttk import Frame, Label, Button

from view.video.video_frame import VideoFrame
from view.video.video_events import Events
from view.search.search_frame import SearchFrame


class MainFrame(Frame):
    """
    Main GUI frame containing all the view components
    """

    def __init__(self, root_tk, width=800, height=600):
        self.root_Tk = root_tk

        Frame.__init__(self, root_tk, width=width, height=height)

        # Event handler in charge of sorting out any user interaction
        self.event_handler = Events(self)

        self.pack(side=TOP, fill=BOTH, expand=True)

        # Status bar - shows name of video selected
        self.status = Label(self, text="Video:", relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        left_frame = Frame(self)
        right_frame = Frame(self)

        left_frame.pack(side=LEFT, )
        right_frame.pack(side=RIGHT)

        search_panel = SearchFrame(left_frame, self.event_handler)
        search_panel.pack()

        self.generate_menubar(root_tk)
        # self.generate_browse_and_search(right_frame)
        self.generate_video(right_frame)

        # Add key bindings
        self.root_Tk.bind("<Control-o>", self.event_handler.on_ctrl_o)
        self.root_Tk.bind("<p>", self.event_handler.on_p)
        self.root_Tk.bind("<m>", self.event_handler.on_m)

    def generate_menubar(self, parent):
        """
        Add a menu bar to the top
        Contain at least the Open option to select a video
        :param parent:
        :return:
        """
        menubar = tk.Menu(parent)
        parent.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Open", underline=0, command=self.event_handler.on_open)
        menubar.add_cascade(label="File", menu=file_menu)

    def generate_video(self, parent):
        """
        Create and add the video GUI components
        :param parent:
        :return: None
        """
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