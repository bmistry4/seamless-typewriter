import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
else:
    import tkinter as Tk
    from tkinter import ttk

from view.tkk_Timer import TkkTimer

class VideoFrame(Tk.Frame):
    """The main window has to deal with events.
    """

    def __init__(self, parent, event_handler):
        Tk.Frame.__init__(self, parent)

        self.parent = parent
        self.event_handler = event_handler

        # The second panel holds controls
        # self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        ctrlpanel = ttk.Frame(self.parent)
        pause = ttk.Button(ctrlpanel, text="Pause", command=self.event_handler.OnPause)
        play = ttk.Button(ctrlpanel, text="Play", command=self.event_handler.OnPlay)
        stop = ttk.Button(ctrlpanel, text="Stop", command=self.event_handler.OnStop)
        volume = ttk.Button(ctrlpanel, text="Volume", command=self.event_handler.OnSetVolume)
        pause.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        volume.pack(side=Tk.LEFT)

        self.volslider = Tk.Scale(ctrlpanel, variable=self.event_handler.volume_var, command=self.event_handler.volume_sel,
                                  from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        self.volslider.pack(side=Tk.LEFT)
        ctrlpanel.pack(side=Tk.BOTTOM)

        ctrlpanel2 = ttk.Frame(self.parent)
        self.timeslider = Tk.Scale(ctrlpanel2, variable=self.event_handler.scale_var, command=self.event_handler.scale_sel,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)

        ctrlpanel2.pack(side=Tk.BOTTOM, fill=Tk.X)


        self.timer = TkkTimer(self.event_handler.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        # self.player.set_hwnd(self.GetHandle()) # for windows, OnOpen does does this
        
        self.event_handler.videopanel = self.videopanel
        self.event_handler.volslider = self.volslider # set in events handler
        self.event_handler.timeslider = self.timeslider #set in event handler

