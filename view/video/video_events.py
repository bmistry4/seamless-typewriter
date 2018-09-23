import itertools
import os
import pathlib
import platform
import queue
import threading
import time
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter as Tk

import vlc
from PIL import Image, ImageTk
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from view.constants import *


class Events:
    """
    Contains the logic for widget bindings e.g. button clicks
    """

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

        # loading stuff
        self.loading = False
        self.loading_canvas = None
        self.loading_frames = None
        self.loading_frame = None
        self.loading_size = 50

        # video buttons
        self._play_pause_button = None

        # video buttons resources
        self.play_image_down_photo = None
        self.play_image_up_photo = None
        self.stop_image_down_photo = None
        self.stop_image_up_photo = None
        self.pause_image_down_photo = None
        self.pause_image_up_photo = None
        self.load_button_photos()

    def load_button_photos(self):
        """
        Create photo variables which are used for setting the video button icons
        :return:
        """
        self.play_image_down_photo = Tk.PhotoImage(file=play_image_down)
        self.play_image_up_photo = Tk.PhotoImage(file=play_image_up)

        self.stop_image_down_photo = Tk.PhotoImage(file=stop_image_down)
        self.stop_image_up_photo = Tk.PhotoImage(file=stop_image_up)

        self.pause_image_down_photo = Tk.PhotoImage(file=pause_image_down)
        self.pause_image_up_photo = Tk.PhotoImage(file=pause_image_up)

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

    def on_space(self, event):
        """
        Key binding for '<space>' which is pause and unpause
        :param event:
        :return: None
        """
        self.on_play_pause()

    def on_p(self, event):
        """
        Key binding for 'p', pause and unpause
        :param event:
        :return: None
        """
        self.on_play_pause()

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
            self.stop_loading_screen()

            self.play()
        except queue.Empty:
            self.parent_frame.after(1000, self.listen_for_thread_completion)

    def on_open(self):
        """
        Pop up a new dialog window to choose a file, then play the selected file
        :return: bool: if video is opened or not
        """
        # if a file is already running, then stop it.
        self.on_stop()

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        fullname = askopenfilename(initialdir=p, title="Choose your file",
                                   filetypes=(("all files", "*.*"), ("mp4 files", "*.mp4")))
        is_updated = self.update_video(fullname)
        return is_updated

    def update_video(self, fullname):
        """
        Update the GUI video with the video file path given as a argument
        :param fullname: video file path (+extension)
        :return: bool on if the video was updated or not
        """
        if os.path.isfile(fullname):

            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            try:
                # Creation
                self.media = self.video_instance.media_new(str(os.path.join(dirname, filename)))
                self._player.set_media(self.media)
            except Exception as err:
                print("ERROR --> Exception thrown in update_video")
                return False

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

            self.display_loading_screen()
            return True
        else:
            return False

    def display_loading_screen(self):
        self.loading_frames = self.load_gif("resources/loading.gif")

        self.loading_frame = self.loading_frames[0]

        self.loading_canvas = Tk.Canvas(self._video_panel, height=self.loading_size)
        self.loading_canvas.create_image(self.loading_canvas.winfo_width() // 2,
                                         self.loading_canvas.winfo_height() // 2,
                                         image=self.loading_frame)
        self.loading_canvas.pack(expand=True, fill=Tk.X)

        self.loading = True
        self.update_loading_screen(0)

    def update_loading_screen(self, index):
        """Because we have to animate gifs ourselves..."""
        index = (index + 1) % len(self.loading_frames)
        self.loading_frame = self.loading_frames[index]

        self.loading_canvas.delete("all")
        self.loading_canvas.create_image(self.loading_canvas.winfo_width() // 2,
                                         self.loading_canvas.winfo_height() // 2,
                                         image=self.loading_frame, anchor=Tk.CENTER)
        if self.loading:
            # if still loading then call this method again to update next frame
            self.parent_frame.after(40, self.update_loading_screen, index)
        else:
            self.loading_canvas.destroy()

    def stop_loading_screen(self):
        self.loading = False

    def load_gif(self, path):
        """Loads each frame (with scaling) into a list"""
        frames = []

        im = Image.open(path)
        try:
            for i in itertools.count(1):
                new_im = Image.new("RGBA", im.size)
                new_im.paste(im)
                new_im.thumbnail((self.loading_size, self.loading_size), Image.ANTIALIAS)
                frames.append(ImageTk.PhotoImage(new_im))
                im.seek(i)
        except EOFError:
            pass  # end of sequence

        return frames

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

    def play(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        :return: bool on if the video was played successfully or not
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if not self._player.get_media():
            is_opened = self.on_open()
            return is_opened
        else:
            # Try to launch the media, if this fails display an error message
            if self._player.play() == -1:
                self.display_error("Unable to play.")
                return False
        return True

    def get_handle(self):
        return self._video_panel.winfo_id()

    def pause(self):
        """Pause the player"""
        self._player.pause()

    def on_stop(self, pause_button=None):
        """Stop the player"""
        self._player.stop()
        # reset the time slider
        self._time_slider.set(0)

        # Make play-pause button show the play icon again
        if pause_button is not None:
            photo = Tk.PhotoImage(file=play_image_up)
            pause_button.config(image=photo)
            pause_button.image = photo  # keep ref so isn't garbage collected

    def on_play_pause(self):
        """
        Event when the play/ pause button is clicked
        If icon is clicked on play -> play video and change icon to pause
        If icon is clicked on paused -> pause video and change icon to play
        This method is called on clicking the button so the resulting icon will be on the hover state
        :return: None
        """
        if self._play_pause_button.is_paused:
            is_playing = self.play()
            # Only change icon if the video can be played
            # This avoids the case then a user cancels a video selection and no video plays (so icon does not change)
            if is_playing:
                self._play_pause_button.config(image=self.pause_image_down_photo)
                self._play_pause_button.is_paused = not self._play_pause_button.is_paused
        else:
            self.pause()
            self._play_pause_button.config(image=self.play_image_down_photo)
            self._play_pause_button.is_paused = not self._play_pause_button.is_paused

    def on_enter_play_pause(self, event):
        """
        On hovering over the play-pause button, change the icon to be in hover state
        :param event: Hover over event
        :return: None
        """
        if self._play_pause_button.is_paused:
            event.widget.config(image=self.play_image_down_photo)
        else:
            event.widget.config(image=self.pause_image_down_photo)

    def on_leave_play_pause(self, event):
        """
        On the mouse leaving the widget. Change the icon to be on the non-hover state
        :param event: Leaving the hover state
        :return: None
        """
        if self._play_pause_button.is_paused:
            event.widget.config(image=self.play_image_up_photo)
        else:
            event.widget.config(image=self.pause_image_up_photo)

    def on_enter_stop(self, event):
        """
        Hovering over the stop button.
        :param event: Hover event
        :return: None
        """
        event.widget.config(image=self.stop_image_down_photo)

    def on_leave_stop(self, event):
        """
        Mouse leaving the stop button
        :param event: Leaving the hover state
        :return: None
        """
        event.widget.config(image=self.stop_image_up_photo)

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
            pass

    def on_toggle_volume(self, evt):
        """Mute/Unmute according to the audio button"""
        is_mute = self._player.audio_get_mute()

        self._player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self._player.audio_get_volume())

    def mute(self):
        """
        Muting/ unmuting the volume
        :return:
        """
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
        edialog = messagebox.showerror(self, 'Error: ' + errormessage)
