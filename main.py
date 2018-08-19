import os
import tkinter as Tk

from controller import Controller
from model.video_searcher import VideoSearcher
from view.main_frame import MainFrame


class ViewMain:
    def __init__(self, controller, title="Seamless Typewriter"):
        # Create a Tk.App(), which handles the windowing system event loop
        self.root = self.tk_get_root()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)
        self.root.winfo_toplevel().title(title)

        MainFrame(self.root, controller)

        # show the player window centred and run the application
        self.root.mainloop()

    def tk_get_root(self):
        if not hasattr(self, "root"):  # (1)
            self.root = Tk.Tk()  # initialization call is inside the function
        return self.root

    def _quit(self):
        print("_quit: bye")
        root = self.tk_get_root()
        root.quit()  # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        os._exit(1)


if __name__ == '__main__':
    # video_path = r"videos\mysql.mp4"
    # searcher = VideoSearcher(video_path=video_path)
    # print(searcher.get_timestamps("add"))
    # print(searcher.get_text(5))

    controller = Controller()
    view = ViewMain(controller)
    controller.set_view(view)


