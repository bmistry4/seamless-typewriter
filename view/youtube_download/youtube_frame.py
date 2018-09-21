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
        url_entry = EntryWithPlaceholder(self, "Enter YouTube URL")
        int_var = Tk.IntVar()
        # Set to be ticked
        int_var.set(1)
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


class EntryWithPlaceholder(Tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
