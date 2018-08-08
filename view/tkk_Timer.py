# import standard libraries
from threading import Thread, Event


class TkkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this"""

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
