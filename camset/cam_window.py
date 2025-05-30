import cv2
import gi
import subprocess

gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, GLib, Gtk


class CamWindow(Gtk.Window):
    def __init__(self, win, dialogs):
        self.win = win
        self.dialogs = dialogs
        self.original_frame_width = 0
        self.original_frame_height = 0
        self.cap = None
        self.run_id = 0

        Gtk.Window.__init__(self, title="Camera feed")
        self.connect(
            "delete-event", lambda w, e: self.stop_camera_feed() or True
        )  # override delete and just hide window, or widgets will be destroyed
        videoframe = self.setup_video()
        self.setup_video_controls(videoframe)

    def stop_camera_feed(self):
        self.cap = None
        self.hide()
        self.win.btn_showcam.set_active(False)
        if self.run_id > 0:
            GLib.source_remove(self.run_id)
        self.run_id = 0

    def setup_video(self):
        # Use a scrolled window that will automatically handle scaling
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)

        # Create image widget that will scale to fit
        self.image = Gtk.Image()
        self.image.set_hexpand(True)
        self.image.set_vexpand(True)

        # Add image to a viewport for proper scaling
        viewport = Gtk.Viewport()
        viewport.add(self.image)
        scrolled.add(viewport)

        self.add(scrolled)
        return scrolled

    def setup_video_controls(self, container):
        # No controls needed for auto-scale only mode
        self.show_all()

    def show_frame(self):
        if self.cap is None:
            return False
        ret, frame = self.cap.read()
        if frame is not None:
            # Store original frame dimensions
            if self.original_frame_width == 0:
                self.original_frame_width = frame.shape[1]
                self.original_frame_height = frame.shape[0]

            # Don't resize the frame - let GTK handle the scaling
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # needed for proper color representation in gtk
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                frame.tostring(),
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                frame.shape[1],
                frame.shape[0],
                frame.shape[2] * frame.shape[1],
            )  # last argument is "rowstride (int) - Distance in bytes between row starts" (??)

            # Get the current window size
            window_width = self.get_allocated_width()
            window_height = self.get_allocated_height()

            if window_width > 1 and window_height > 1:
                # Calculate scaled size maintaining aspect ratio
                scale_x = window_width / frame.shape[1]
                scale_y = window_height / frame.shape[0]
                scale = min(scale_x, scale_y)

                new_width = int(frame.shape[1] * scale)
                new_height = int(frame.shape[0] * scale)

                # Scale the pixbuf to fit the window
                scaled_pixbuf = pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.BILINEAR)
                self.image.set_from_pixbuf(scaled_pixbuf)
            else:
                # Fallback to original size if window size not available
                self.image.set_from_pixbuf(pixbuf.copy())

        return True

    def start_camera_feed(self, pixelformat, vfeedwidth, vfeedheight, fourcode):
        card = self.win.card

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
        )
        out, err = process.communicate()
        if process.returncode == 0:
            cap = cv2.VideoCapture(card, cv2.CAP_V4L2)
            # also set resolution to cap, otherwise cv2 will use default and not the res set by v4l2
            cap.set(3, int(vfeedwidth))
            cap.set(4, int(vfeedheight))
            cap.set(cv2.CAP_PROP_FOURCC, fourcode)
            # cap.set(5,1) 1 fps
            self.cap = cap
            return GLib.idle_add(self.show_frame)
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
        self.run_id = self.start_camera_feed(list[0], list[1], list[2], list[3])
        if self.run_id > 0:
            self.win.btn_showcam.set_active(True)
            self.show()
        else:
            self.stop_camera_feed()

