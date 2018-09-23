import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
else:
    import tkinter as Tk
    from tkinter.constants import *
    from tkinter import ttk

from view.video.tkk_timer import TkkTimer
from functools import partial
from view.constants import *

class VideoFrame(Tk.Frame):
    """The main window (frame) containing all video related GUI components. This includes: the video, and all video
    button commands
    """

    def __init__(self, parent, event_handler):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.event_handler = event_handler

        self.is_paused = True
        self.play_pause_button = None
        self.stop_button = None

        self.play_image_down_photo = None
        self.play_image_up_photo = None
        self.stop_image_down_photo = None
        self.stop_image_up_photo = None
        self.pause_image_down_photo = None
        self.pause_image_up_photo = None
        self.load_button_photos()

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

    def load_button_photos(self):
        self.play_image_down_photo = Tk.PhotoImage(file=play_image_down)
        self.play_image_up_photo = Tk.PhotoImage(file=play_image_up)
        self.stop_image_down_photo = Tk.PhotoImage(file=stop_image_down)
        self.stop_image_up_photo = Tk.PhotoImage(file=stop_image_up)
        self.pause_image_down_photo = Tk.PhotoImage(file=pause_image_down)
        self.pause_image_up_photo = Tk.PhotoImage(file=pause_image_up)

    def generate_video_panel(self, parent):
        """
        Panel which displays the video
        :param parent: Parent panel/ frame
        :return: None
        """
        canvas = Tk.Canvas(parent)
        canvas.pack(fill=Tk.BOTH, expand=1)


    def action(self, is_paused=[True]):
        """
        toggle the button with up/down images,
        using a list element as static variable
        """
        if is_paused[0]:
            self.play_pause_button.config(image=self.play_image_down_photo)
            is_paused[0] = False
        else:
            self.play_pause_button.config(image=self.play_image_up_photo)
            is_paused[0] = True

    def on_play_pause(self):
        if self.is_paused:
            is_playing = self.event_handler.play()
            if is_playing:
                self.play_pause_button.config(image=self.pause_image_down_photo)
                self.is_paused = not self.is_paused
        else:
            self.event_handler.pause()
            self.play_pause_button.config(image=self.play_image_down_photo)
            self.is_paused = not self.is_paused


    def on_enter_play_pause(self, event):
        if self.is_paused:
            self.play_pause_button.config(image=self.play_image_down_photo)
        else:
            self.play_pause_button.config(image=self.pause_image_down_photo)


    def on_leave_play_pause(self, event):
        if self.is_paused:
            self.play_pause_button.config(image=self.play_image_up_photo)
        else:
            self.play_pause_button.config(image=self.pause_image_up_photo)

    def on_enter_stop(self, event):
        self.stop_button.config(image=self.stop_image_down_photo)

    def on_leave_stop(self, event):
        self.stop_button.config(image=self.stop_image_up_photo)


    def generate_control_panel(self, parent):
        """
        Create the buttons used for user options to control the video (e.g. play, pause, stop...)
        :param parent:
        :return:
        """
        self.play_pause_button = Tk.Button(parent, image=self.play_image_up_photo, bd=0, command=self.on_play_pause)
        self.play_pause_button.bind("<Enter>", self.on_enter_play_pause)
        self.play_pause_button.bind("<Leave>", self.on_leave_play_pause)

        self.stop_button = Tk.Button(parent, image=self.stop_image_up_photo, bd=0,
                                     command=partial(self.event_handler.on_stop, pause_button=self.play_pause_button))
        self.stop_button.bind("<Enter>", self.on_enter_stop)
        self.stop_button.bind("<Leave>", self.on_leave_stop)

        self.play_pause_button.pack(padx=10, side=Tk.LEFT)
        self.stop_button.pack(padx=10, side=Tk.LEFT)

        # Volume control
        volslider = ttk.Scale(parent, variable=self.event_handler.volume_var,
                              command=self.event_handler.volume_sel,
                              from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        volslider.set(100)
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
