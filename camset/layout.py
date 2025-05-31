import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Layout:
    def __init__(self, win, dialogs):
        self.win = win
        self.dialogs = dialogs

    def setup_main_container(self):
        self.win.layout = Gtk.ScrolledWindow()
        self.win.layout.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.win.layout.set_hexpand(True)
        self.win.layout.set_vexpand(True)
        self.win.add(self.win.layout)

        # Use a Box instead of Grid for better flexibility
        self.win.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.win.main_box.set_margin_start(10)
        self.win.main_box.set_margin_end(10)
        self.win.main_box.set_margin_top(10)
        self.win.main_box.set_margin_bottom(10)
        self.win.layout.add(self.win.main_box)

    def setup_boxes(self):
        # Create responsive container that can switch between horizontal and vertical layout
        self.win.control_sections_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.win.control_sections_box.set_hexpand(True)
        self.win.control_sections_box.set_vexpand(True)

        # Menu controls section - just the control box, labels are integrated
        self.win.menu_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.win.menu_control_box = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)

        # Bool controls section - just the control box, labels are integrated
        self.win.bool_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.win.bool_control_box = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)

        # Int controls section - just the control box, labels are integrated
        self.win.int_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.win.int_control_box = Gtk.Box(spacing=3, orientation=Gtk.Orientation.VERTICAL)

        # Device selection
        self.win.devicelabelbox = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
        self.win.devicecontrolbox = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)

    def setup_device_selection_box(self):
        self.win.device_selection = Gtk.ComboBox()
        self.win.device_selection.set_hexpand(True)
        # Reduce the height of the combobox
        self.win.device_selection.set_size_request(-1, 30)
        self.win.label = Gtk.Label(label="Device")
        self.win.label.set_halign(Gtk.Align.START)
        self.win.devicecontrolbox.pack_start(self.win.device_selection, True, True, 0)
        self.win.store = Gtk.ListStore(str)
        cell = Gtk.CellRendererText()
        self.win.device_selection.pack_start(cell, True)
        self.win.device_selection.add_attribute(cell, "text", 0)
        self.win.device_selection.set_model(self.win.store)
        self.win.devicelabelbox.pack_start(self.win.label, False, False, 0)

    def setup_buttons(self):
        # Create a horizontal box for buttons
        self.win.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.win.button_box.set_halign(Gtk.Align.CENTER)

        self.win.btn_defaults = Gtk.Button(label="Load defaults")
        self.win.btn_defaults.set_size_request(-1, 30)  # Reduce button height
        self.win.btn_defaults.connect("clicked", self.win.on_btn_defaults_clicked)

        self.win.btn_showcam = Gtk.ToggleButton(label="Show camera feed")
        self.win.btn_showcam.set_size_request(-1, 30)  # Reduce button height
        self.win.btn_showcam.connect("toggled", self.win.on_btn_showcam_toggled)

        self.win.button_box.pack_start(self.win.btn_defaults, False, False, 0)
        self.win.button_box.pack_start(self.win.btn_showcam, False, False, 0)

    def setup_warning_container(self):
        self.win.warningcontainer = Gtk.Box(hexpand=True)
        self.win.warning = Gtk.Revealer(hexpand=True)
        self.win.warning.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.win.warning.props.transition_duration = 1250
        self.win.warning.set_reveal_child(False)
        self.win.warningmessage = Gtk.TextView()
        self.win.warningmessage.set_editable(False)
        self.win.warningmessage.set_left_margin(10)
        self.win.warningmessage.set_right_margin(10)
        self.win.warningmessage.set_top_margin(5)
        self.win.warningmessage.set_bottom_margin(5)
        self.win.warningmessage.props.halign = Gtk.Align.CENTER
        self.win.warning.add(self.win.warningmessage)
        self.win.warningcontainer.add(self.win.warning)

    def setup_toolbar(self, path, v4l2_control):
        openbtn = Gtk.ToolButton()
        openbtn.set_label("Load settings")
        openbtn.set_is_important(True)
        openbtn.set_icon_name("gtk-open")
        openbtn.connect("clicked", self.dialogs.on_open_clicked, self.win, path, v4l2_control)

        savebtn = Gtk.ToolButton()
        savebtn.set_label("Save settings")
        savebtn.set_is_important(True)
        savebtn.set_icon_name("gtk-save")
        savebtn.connect("clicked", self.dialogs.on_save_clicked, self.win, path, v4l2_control)

        self.win.autoload_checkbutton = Gtk.ToggleToolButton()
        self.win.autoload_checkbutton.set_label("Autoload settings")
        self.win.autoload_checkbutton.set_active(True)

        self.win.toolbar = Gtk.Toolbar()
        self.win.toolbar.add(openbtn)
        self.win.toolbar.add(savebtn)
        self.win.toolbar.add(self.win.autoload_checkbutton)

    def setup_grid(self):
        # Create device selection row
        device_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        device_row.pack_start(self.win.devicelabelbox, False, False, 0)
        device_row.pack_start(self.win.devicecontrolbox, True, True, 0)
        device_row.pack_start(self.win.button_box, False, False, 0)

        # Pack everything into main vertical box
        self.win.main_box.pack_start(self.win.toolbar, False, False, 0)
        self.win.main_box.pack_start(self.win.warningcontainer, False, False, 0)
        self.win.main_box.pack_start(device_row, False, False, 0)

        # Slider controls first (don't expand - just take what they need)
        int_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        int_container.set_margin_top(5)
        int_container.add(self.win.int_control_box)
        self.win.main_box.pack_start(int_container, False, False, 0)

        # Dropdown controls second
        menu_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        menu_container.set_margin_top(5)
        menu_container.add(self.win.menu_control_box)
        self.win.main_box.pack_start(menu_container, False, False, 0)

        # Switch controls last (allow this section to expand and fill extra space)
        bool_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        bool_container.set_margin_top(5)
        bool_container.add(self.win.bool_control_box)
        self.win.main_box.pack_start(bool_container, True, True, 0)

    def setup_resolution(self):
        # Create horizontal box for resolution label and control
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        label = Gtk.Label()
        label.set_text("Video Resolution")
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.CENTER)
        label.set_size_request(180, 25)  # Increased to 180 for more uniform appearance
        hbox.pack_start(label, False, False, 0)

        self.win.resolution_selection = Gtk.ComboBox()
        self.win.resolution_selection.set_hexpand(True)
        self.win.resolution_selection.set_size_request(300, 30)  # Set consistent minimum width
        cell = Gtk.CellRendererText()
        self.win.resolution_selection.pack_start(cell, True)
        self.win.resolution_selection.add_attribute(cell, "text", 0)
        self.win.resolution_selection.set_model(self.win.ctrl_store)
        self.win.resolution_selection.connect("changed", self.win.on_resolution_changed)
        hbox.pack_start(self.win.resolution_selection, True, True, 0)

        self.win.menu_control_box.pack_start(hbox, False, False, 0)

    def add_menu_item(self, setting, action):
        self.win.ctrl_combobox = Gtk.ComboBox()
        self.win.ctrl_combobox.set_hexpand(True)
        self.win.ctrl_combobox.set_size_request(-1, 30)  # Reduce height
        self.win.ctrl_store = Gtk.ListStore(str)
        cell = Gtk.CellRendererText()
        self.win.ctrl_combobox.pack_start(cell, True)
        self.win.ctrl_combobox.add_attribute(cell, "text", 0)
        self.win.ctrl_combobox.set_model(self.win.ctrl_store)
        self.win.ctrl_combobox.connect("changed", action, setting)
        self.win.menu_control_box.pack_start(self.win.ctrl_combobox, True, True, 0)

    def add_int_item(self, line, setting, value, action):
        upper = line.split("max=", 1)[1]
        upper = int(upper.split(" ", 1)[0])
        lower = line.split("min=", 1)[1]
        lower = int(lower.split(" ", 1)[0])
        step = line.split("step=", 1)[1]
        step = int(step.split(" ", 1)[0])
        adj = Gtk.Adjustment(value=value, lower=lower, upper=upper, step_increment=step, page_increment=1, page_size=0)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.RIGHT)
        scale.set_hexpand(True)
        scale.set_size_request(200, 30)  # Set minimum width and reduce height
        scale.connect("value-changed", action, setting)
        self.win.int_control_box.pack_start(scale, True, True, 0)

    def add_bool_item(self, setting, value, action):
        switch = Gtk.Switch()
        if value == 1:
            switch.set_active(True)
        else:
            switch.set_active(False)
        switch.connect("notify::active", action, setting)
        switch.set_halign(Gtk.Align.START)
        switch.set_valign(Gtk.Align.CENTER)
        self.win.bool_control_box.pack_start(switch, False, False, 0)

    def add_menu_item_with_label(self, setting, action, label):
        # Create a horizontal box for this label-control pair
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Add the label
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.CENTER)
        label.set_size_request(180, 25)  # Increased to 180 for more uniform appearance
        hbox.pack_start(label, False, False, 0)

        # Create the combobox
        self.win.ctrl_combobox = Gtk.ComboBox()
        self.win.ctrl_combobox.set_hexpand(True)
        self.win.ctrl_combobox.set_size_request(300, 30)  # Set consistent minimum width
        self.win.ctrl_store = Gtk.ListStore(str)
        cell = Gtk.CellRendererText()
        self.win.ctrl_combobox.pack_start(cell, True)
        self.win.ctrl_combobox.add_attribute(cell, "text", 0)
        self.win.ctrl_combobox.set_model(self.win.ctrl_store)
        self.win.ctrl_combobox.connect("changed", action, setting)
        hbox.pack_start(self.win.ctrl_combobox, True, True, 0)

        # Add the horizontal box to the menu control box
        self.win.menu_control_box.pack_start(hbox, False, False, 0)

    def add_int_item_with_label(self, line, setting, value, action, label):
        # Create a horizontal box for this label-control pair
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Add the label
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.CENTER)
        label.set_size_request(180, 25)  # Increased to 180 for more uniform appearance
        hbox.pack_start(label, False, False, 0)

        # Create the slider
        upper = line.split("max=", 1)[1]
        upper = int(upper.split(" ", 1)[0])
        lower = line.split("min=", 1)[1]
        lower = int(lower.split(" ", 1)[0])
        step = line.split("step=", 1)[1]
        step = int(step.split(" ", 1)[0])
        adj = Gtk.Adjustment(value=value, lower=lower, upper=upper, step_increment=step, page_increment=1, page_size=0)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_digits(0)
        scale.set_value_pos(Gtk.PositionType.RIGHT)
        scale.set_hexpand(True)
        scale.set_size_request(300, 30)  # Set consistent minimum width to match dropdowns
        scale.connect("value-changed", action, setting)
        hbox.pack_start(scale, True, True, 0)

        # Add the horizontal box to the int control box
        self.win.int_control_box.pack_start(hbox, False, False, 0)

    def add_bool_item_with_label(self, setting, value, action, label):
        # Create a horizontal box for this label-control pair
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Add the label
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.CENTER)
        label.set_size_request(180, 25)  # Increased to 180 for more uniform appearance
        hbox.pack_start(label, False, False, 0)

        # Create the switch
        switch = Gtk.Switch()
        if value == 1:
            switch.set_active(True)
        else:
            switch.set_active(False)
        switch.connect("notify::active", action, setting)
        switch.set_halign(Gtk.Align.START)
        switch.set_valign(Gtk.Align.CENTER)
        hbox.pack_start(switch, False, False, 0)

        # Add the horizontal box to the bool control box
        self.win.bool_control_box.pack_start(hbox, False, False, 0)

