import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk
    from tkinter.constants import *

from functools import partial


class YoutubeFrame(Tk.Frame):
    def __init__(self, parent, event_handler):
        Tk.Frame.__init__(self, parent, background="black")
        self._event_handler = event_handler


        # Create gui components and pack them
        url_entry = Tk.Entry(self)
        int_var = Tk.IntVar()
        play_checkbox = Tk.Checkbutton(self, text="Auto-play", variable=int_var)
        download_button = Tk.Button(self, text="Download",
                                    command=partial(self.event_handler.on_youtube_download,
                                                    url_entry=url_entry,
                                                    checkbox_sel=int_var))

        url_entry.pack(fill=X, expand=True, padx=10, side=LEFT)
        play_checkbox.pack(fill=X, padx=10, side=LEFT)
        download_button.pack(fill=X, padx=10, side=LEFT)

    @property
    def event_handler(self):
        return self._event_handler
