import threading
import tkinter as tk
from tkinter import filedialog
import pygame
import vlc

WIDTH = 800
HEIGHT = 600

class MainFrame(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.file = '' # method to browse music files in system
        self.player = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = (screen_width / 2) - (WIDTH / 2)  # set location of window to middle of screen
        center_y = (screen_height / 2) - (HEIGHT / 2)
        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, center_x, center_y))

        # videoPlayer = vlc.MediaPlayer("")
        pygame.init()
        pygame.mixer.init()

        self.t2 = None

        self.initUI()

        self.mainloop()
        pygame.quit()

    def initUI(self):
        # video portion
        playButton = tk.Button(self, text="Play video", command=self.playVideo)
        pauseVideo = tk.Button(self, text="Pause video", command=self.pauseVideo)
        stopVideo = tk.Button(self, text="Stop video", command=self.stopVideo)

        browseButton = tk.Button(self, text="Browse files", command=self.browse)
        self.bind("<x>", self.stopUtility)
        self.bind("<space>", self.pauseVideoUtility) # binding keyboard shortcuts to buttons on window
        self.focus_set()

        playButton.pack(pady=10)
        pauseVideo.pack(pady=10)
        stopVideo.pack(pady=10)
        browseButton.pack(pady=10)

    def browse(self):  # to change value of a global variable inside a function apply global
        self.filename = filedialog.askopenfilename(initialdir="/home/${USER}/", title="Choose Music file")
        self.file = self.filename

    def stopUtility(self, event):  # stop video
        if self.player is not None:
            self.t2.join()
            self.player.stop()


    def startVideo(self, file):  # play video designated by file variable
        self.player = vlc.MediaPlayer(file)
        self.player.play()

    def playVideo(self):
        if self.file != "":
            self.t2 = threading.Thread(target=self.startVideo, args=(self.file,))
            self.t2.start()

    def stopVideo(self):
        if self.player is not None:
            self.t2.join()  # wait for music thread to join main thread
            self.player.stop()
            self.file = ""

    def pauseVideoUtility(self, event):
        self.pauseVideo()

    def pauseVideo(self):
        if self.player is not None:
            self.player.pause()

MainFrame()