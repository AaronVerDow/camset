import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class CamWindow:
    def __init__(self, win, dialogs):
        self.win = win
        self.dialogs = dialogs
        self.ffplay_process = None

    def stop_camera_feed(self):
        if self.ffplay_process and self.ffplay_process.poll() is None:
            self.ffplay_process.terminate()
            try:
                self.ffplay_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.ffplay_process.kill()
        self.ffplay_process = None
        self.win.btn_showcam.set_active(False)

    def start_camera_feed(self, pixelformat, vfeedwidth, vfeedheight, fourcode=None):
        card = self.win.card

        # Set the video format using v4l2-ctl
        process = subprocess.Popen(
            [
                "v4l2-ctl",
                "-d",
                card,
                "-v",
                "height={0},width={1},pixelformat={2}".format(vfeedheight, vfeedwidth, pixelformat),
            ],
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = process.communicate()
        
        if process.returncode == 0:
            # Start ffplay with the video device
            try:
                self.ffplay_process = subprocess.Popen(
                    ["ffplay", "-f", "v4l2", card],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return 1  # Success
            except FileNotFoundError:
                self.dialogs.show_message("ffplay not found. Please install ffmpeg.", True, self.win)
                return 0
            except Exception as e:
                self.dialogs.show_message(f"Unable to start ffplay: {e}", True, self.win)
                return 0
        else:
            if "Device or resource busy" in str(out):
                errorMsg = "Unable to start feed, the device is busy"
            elif process.returncode == 1:
                errorMsg = "Unable to start feed, not a valid output device"
            else:
                errorMsg = "Unable to start feed, unknown error"
            self.dialogs.show_message(errorMsg, True, self.win)
        return 0

    def init_camera_feed(self, list):
        success = self.start_camera_feed(list[0], list[1], list[2], list[3])
        if success > 0:
            self.win.btn_showcam.set_active(True)
        else:
            self.stop_camera_feed()

    # Keep these methods for compatibility but make them no-ops
    def hide(self):
        self.stop_camera_feed()
    
    def set_title(self, title):
        pass
    
    @property
    def props(self):
        class Props:
            @property
            def visible(self):
                return self.ffplay_process is not None and self.ffplay_process.poll() is None
        
        props_instance = Props()
        props_instance.ffplay_process = self.ffplay_process
        return props_instance

