import os
import pathlib
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import platform
import time
import vlc
import tkinter as Tk
from tkinter import messagebox

class Events:

    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.player = None
        self.videopanel  = None
        self.volslider = None
        self.timeslider = None


        # VLC player controls
        self.video_instance = vlc.Instance()
        self.player = self.video_instance.media_player_new()

        self.volume_var = Tk.IntVar()

        # Time slider variables
        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider_last_update = time.time()


    def on_exit(self, evt):
        """Closes the window.
        """
        self.Close()

    def on_open(self):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.on_stop()

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        fullname = askopenfilename(initialdir=p, title="choose your file",
                                   filetypes=(("all files", "*.*"), ("mp4 files", "*.mp4")))
        if os.path.isfile(fullname):
            print(fullname)
            splt = os.path.split(fullname)
            dirname = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.Media = self.video_instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)

            # Report the title of the file chosen
            title = self.player.get_title()
            #  if an error was encountred while retriving the title, then use  filename
            if title == -1:
               title = filename

            self.parent_frame.update_status_bar(title)

            # set the window id where to render VLC's video output
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.get_handle())
            else:
                self.player.set_xwindow(self.get_handle())  # this line messes up windows
            # FIXME: this should be made cross-platform
            self.on_play()

            # set the volume slider to the current volume
            # self.volslider.SetValue(self.player.audio_get_volume() / 2)
            self.volslider.set(self.player.audio_get_volume())

    def on_play(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if not self.player.get_media():
            self.on_open()
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.display_error("Unable to play.")

    def get_handle(self):
        return self.videopanel.winfo_id()

    # def OnPause(self, evt):
    def on_pause(self):
        """Pause the player.
        """
        self.player.pause()

    def on_stop(self):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def on_timer(self):
        """Update the time slider according to the current movie time.
        """
        if self.player == None:
            return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
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
            self.player.set_time(int(mval))  # expects milliseconds

    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.display_error("Failed to set volume")

    def on_toggle_volume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self.player.audio_get_volume())

    def on_set_volume(self):
        """Set the volume according to the volume sider.
        """
        volume = self.volume_var.get()
        print("volume= ", volume)
        # volume = self.volslider.get() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.display_error("Failed to set volume")

    def display_error(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = messagebox.showerror(self, 'Error '+ errormessage)




