import vlc
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

# import standard libraries
import os
import pathlib
from threading import Timer, Thread, Event
import time
import platform


class TkkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        # print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            # print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters
