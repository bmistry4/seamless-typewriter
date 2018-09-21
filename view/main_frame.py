import tkinter as tk
from tkinter import Frame
from tkinter.constants import *
from tkinter.ttk import Label

from view.video.video_frame import VideoFrame
from view.video.video_events import Events
from view.search.search_frame import SearchFrame
from view.youtube_download.youtube_frame import YoutubeFrame

class MainFrame(Frame):
    """
    Main GUI frame containing all the view components
    """

    def __init__(self, root_tk, controller, width=800, height=600):
        self.root_Tk = root_tk
        self.controller = controller

        Frame.__init__(self, root_tk, width=width, height=height)

        # Event handler in charge of sorting out any user interaction
        self.event_handler = Events(self, controller)

        self.pack(side=TOP, fill=BOTH, expand=True)

        # Status bar - shows name of video selected
        self.status = Label(self, text="Video:", relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)

        # Create and add left and right top frames to the root frame
        left_frame = Frame(self)
        right_frame = Frame(self)

        # BIG SECRET - fill=BOTH, expand=True = makes stuff resizable
        left_frame.pack(fill=BOTH, expand=True, side=LEFT)
        right_frame.pack(fill=BOTH, expand=True, side=RIGHT)

        # Create menu bar
        self.generate_menubar(root_tk)

        # Create search stuff
        search_panel = SearchFrame(left_frame, self.event_handler, self.controller)
        search_panel.pack()

        # Create video stuff
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
        file_menu.add_command(label="Youtube Download", command=self.event_handler.on_youtube_download)

        menubar.add_cascade(label="File", menu=file_menu)

    def generate_video(self, parent):
        """
        Create and add the video GUI components
        :param parent:
        :return: None
        """
        video = VideoFrame(parent, self.event_handler)
        video.pack()
        video.pack(expand=True)

        # Create youtube download stuff
        youtube_panel = YoutubeFrame(parent, self.event_handler)
        youtube_panel.pack(fill=BOTH , expand=True)


    def update_status_bar(self, text):
        """
        Updates the status bar on main frame

        :param
            text: New text for status bar
        :return:
            None
        """
        self.status['text'] = text
