import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
else:
    import tkinter as Tk
    from tkinter.constants import *
    from tkinter import ttk

from view.video.tkk_timer import TkkTimer


class VideoFrame(Tk.Frame):
    """The main window (frame) containing all video related GUI components. This includes: the video, and all video
    button commands
    """

    def __init__(self, parent, event_handler):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.event_handler = event_handler

        # Create video panel
        video_panel = ttk.Frame(self.parent)
        self.generate_video_panel(video_panel)

        # Create the video control buttons
        video_control_panel = ttk.Frame(self.parent)
        volume_slider = self.generate_control_panel(video_control_panel)

        # Create the timer slider for the video
        time_slider_panel = ttk.Frame(self.parent)
        time_slider = self.generate_time_slider(time_slider_panel)

        self.begin_timer()
        self.parent.update()

        # self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this

        # set in events handler
        self.event_handler._video_panel = video_panel
        self.event_handler._volume_slider = volume_slider
        self.event_handler._time_slider = time_slider

        # Deal with layout of sub-frames (containers)
        # Let the video expand on resizing and let the slider expand on the X only. Let controls just be added below
        # the slider
        video_panel.pack(fill=BOTH, expand=True)
        time_slider_panel.pack(fill=X)
        video_control_panel.pack()

        # Makes resizable
        self.pack(fill=BOTH, expand=True)

    def generate_video_panel(self, parent):
        """
        Panel which displays the video
        :param parent: Parent panel/ frame
        :return: None
        """
        canvas = Tk.Canvas(parent)
        canvas.pack(fill=Tk.BOTH, expand=1)

    def generate_control_panel(self, parent):
        """
        Create the buttons used for user options to control the video (e.g. play, pause, stop...)
        :param parent:
        :return:
        """
        pause = ttk.Button(parent, text="Pause", command=self.event_handler.on_pause)
        play = ttk.Button(parent, text="Play", command=self.event_handler.on_play)
        stop = ttk.Button(parent, text="Stop", command=self.event_handler.on_stop)

        pause.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)

        # Volume control
        volslider = Tk.Scale(parent, variable=self.event_handler.volume_var,
                             command=self.event_handler.volume_sel,
                             from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        volslider.pack(side=Tk.LEFT)
        return volslider

    def generate_time_slider(self, parent):
        """
        Create a time slider responsible for keeping track of how far a video has played
        :param parent: Parent panel/ frame
        :return: The timer slider
        """
        timeslider = Tk.Scale(parent, variable=self.event_handler.scale_var, command=self.event_handler.scale_sel,
                              from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        timeslider.pack(side=BOTTOM, fill=X, expand=1)
        return timeslider

    def begin_timer(self):
        """
        Start a timer in a new thread
        :return: None
        """
        self.timer = TkkTimer(self.event_handler.on_timer, 1.0)
        self.timer.start()
