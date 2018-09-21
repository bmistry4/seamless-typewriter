import os
import pathlib
import platform
import queue
import threading
import time
import tkinter as Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

import vlc
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class Events:
    def __init__(self, parent_frame, controller):
        self.parent_frame = parent_frame
        self.controller = controller
        self.prev_vol = 0

        self._video_panel = None
        self._volume_slider = None
        self._time_slider = None

        # VLC player controls
        self.video_instance = vlc.Instance()
        self._player = self.video_instance.media_player_new()

        self.volume_var = Tk.IntVar()

        # Time slider variables
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider_last_update = time.time()

    def on_exit(self, evt):
        """Closes the window"""
        self.Close()

    # When control-o pressed
    def on_ctrl_o(self, event):
        """
        When ctrl-o is pressed open a file fialog to select a video
        :param event: Event from clicking the key binding
        :return: None
        """
        self.on_open()

    def on_p(self, event):
        """
        Key binding for 'p', pause and unpause
        :param event:
        :return: None
        """
        self.on_pause()

    def on_m(self, event):
        """
        Key binding for 'm', mute and unmute
        :param event:
        :return:
        """
        self.on_toggle_volume(event)

    def listen_for_thread_completion(self):
        """Check if there is something in the queue"""
        try:
            self.thread_queue.get(False)
        except queue.Empty:
            self.parent_frame.after(1000, self.listen_for_thread_completion)

    def on_open(self):
        """Pop up a new dialow window to choose a file, then play the selected file"""
        # if a file is already running, then stop it.
        self.on_stop()

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        fullname = askopenfilename(initialdir=p, title="Choose your file",
                                   filetypes=(("all files", "*.*"), ("mp4 files", "*.mp4")))

        self.update_video(fullname)

    def update_video(self, fullname):
        """
        Update the GUI video with the video file path given as a argument
        :param fullname: video file path (+extension)
        :return:
        """
        if os.path.isfile(fullname):

            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.media = self.video_instance.media_new(str(os.path.join(dirname, filename)))
            self._player.set_media(self.media)

            # Report the title of the file chosen
            title = self._player.get_title()
            #  if an error was encountered while retrieving the title, then use filename
            if title == -1:
                title = filename

            self.parent_frame.update_status_bar(title)

            # set the window id where to render VLC's video output
            if platform.system() == 'Windows':
                self._player.set_hwnd(self.get_handle())
            else:
                self._player.set_xwindow(self.get_handle())  # this line messes up windows

            self.thread_queue = queue.Queue()
            self.new_thread = threading.Thread(
                target=self.controller.index_video,
                kwargs={
                    'path': fullname,
                    'thread_queue': self.thread_queue})
            self.new_thread.start()
            self.parent_frame.after(1000, self.listen_for_thread_completion)

            self.on_play()

            # set the volume slider to the current volume
            # self.volslider.SetValue(self.player.audio_get_volume() / 2)
            self._volume_slider.set(self._player.audio_get_volume())

    def file_save_dialog(self):
        """
        Open a save dialog to get a path where the user wants to save the downloaded youtube video to
        :return: str/ bool - filepath or False if cancel was clicked
        """
        file = asksaveasfile(defaultextension=".mp4")
        if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return False
        filename = file.name
        file.close()
        return filename

    def on_youtube_download(self, url_entry):
        """
        Download and potentially play given youtube url
        :param url_entry: field widget reference for entering the url
        :return:
        """
        # Get the file path and file name to save the video too
        fullname = self.file_save_dialog()
        # Meaning the cancel button isn't clicked
        if fullname is not False:
            save_location = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            filename, extension = os.path.splitext(filename)
            print("Downloading from youtube...")
            try:
                yt = YouTube(url_entry.get())
                # Only get mp4 streams and choose the highest quality download
                yt.streams.filter(subtype='mp4').first().download(output_path=save_location, filename=filename)
            except RegexMatchError as err:
                print("ERROR --> RegexMatchError: Invalid URL. Exiting Method")
                return False
            print("... 100% downloaded")
            Tk.messagebox.showinfo("Successful Download", "Video downloaded")

            # Start playing downloaded video
            # Stop and currently playing videos
            self.on_stop()
            # Update the canvas with the new video
            self.update_video(fullname)

    def on_play(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if not self._player.get_media():
            self.on_open()
        else:
            # Try to launch the media, if this fails display an error message
            if self._player.play() == -1:
                self.display_error("Unable to play.")

    def get_handle(self):
        return self._video_panel.winfo_id()

    def on_pause(self):
        """Pause the player"""
        self._player.pause()

    def on_stop(self):
        """Stop the player"""
        self._player.stop()
        # reset the time slider
        self._time_slider.set(0)

    def on_timer(self):
        """Update the time slider according to the current movie time"""
        if self._player is None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self._player.get_length()
        dbl = length * 0.001
        self._time_slider.config(to=dbl)

        # update the time on the slider
        tyme = self._player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programmatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self._time_slider.set(dbl)

    def scale_sel(self, evt):
        if self._player is None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            # this is a hack. The timer updates the time slider.
            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
            # I can't tell the difference between when the user has manually moved the slider and when
            # the timer changed the slider. But when the user moves the slider tkinter only notifies
            # this rtn about once per second and when the slider has quit moving.
            # Also, the tkinter notification value has no fractional seconds.
            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
            # we know that this notification is due to the timer changing the slider.
            # otherwise the notification is due to the user changing the slider.
            # if the user is changing the slider then I have the timer routine wait for at least
            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
            # user)
            # selection = "Value, last = " + sval + " " + str(self.timeslider_last_val)
            # print("selection= ", selection)
            self.timeslider_last_update = time.time()

            mval = "%.0f" % (nval * 1000)
            self._player.set_time(int(mval))  # expects milliseconds

    def volume_sel(self, evt):
        if self._player is None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self._player.audio_set_volume(volume) == -1:
            self.display_error("Failed to set volume")

    def on_toggle_volume(self, evt):
        """Mute/Unmute according to the audio button"""
        is_mute = self._player.audio_get_mute()

        self._player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self._player.audio_get_volume())

    def mute(self):
        current_vol = self.volume_var.get()
        if current_vol != 0:
            self.prev_vol = current_vol
            # model component update
            self.volume_var.set(0)

            # view component update
            self._volume_slider.set(0)
        else:
            self.volume_var.set(self.prev_vol)
            self._volume_slider.set(self.prev_vol)

    def display_error(self, errormessage):
        """Display a simple error dialog"""
        messagebox.showerror(self, 'Error ' + errormessage)
