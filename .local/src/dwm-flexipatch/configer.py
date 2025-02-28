#!/usr/bin/env python3
import os
import re
import json
import shutil
import subprocess
import datetime
from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango, Gio

class DWMConfig:
    def __init__(self):
        self.dwm_path = self.find_dwm_path()
        self.config_files = self.find_config_files()
        self.patches = self.parse_patches()
        self.config = self.parse_config()
        self.categories = {
            'Appearance': [],
            'Keybinds': [],
            'Rules': [],
            'Scratchpads': [],
            'Autostart': [],
            'Patches': []
        }
        self.organize_config()

    def find_dwm_path(self):
        common_paths = [
            os.path.expanduser('~/dwm'),
            '/usr/local/src/dwm',
            '/opt/dwm'
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None

    def find_config_files(self):
        if not self.dwm_path:
            return {}
        
        files = {}
        for f in ['config.h', 'config.def.h', 'patches.h']:
            path = os.path.join(self.dwm_path, f)
            if os.path.exists(path):
                with open(path, 'r') as file:
                    files[f] = file.read()
        return files

    def create_backup(self):
        if not self.dwm_path:
            return False
            
        backup_dir = os.path.expanduser('~/.dwm/backups')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'dwm_backup_{timestamp}')
        
        try:
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copytree(self.dwm_path, backup_path)
            return True
        except Exception as e:
            print(f"Backup failed: {e}")
            return False

    def build_dwm(self, password):
        if not self.dwm_path:
            return False, "DWM source directory not found"
            
        try:
            # Create backup before building
            if not self.create_backup():
                return False, "Backup creation failed"
                
            # Build commands
            commands = [
                ['sudo', '-S', 'make', 'clean'],
                ['sudo', '-S', 'make'],
                ['sudo', '-S', 'make', 'install']
            ]
            
            for cmd in commands:
                process = subprocess.Popen(
                    cmd,
                    cwd=self.dwm_path,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Send password to sudo
                stdout, stderr = process.communicate(input=f"{password}\n")
                
                if process.returncode != 0:
                    return False, f"Command failed: {stderr}"
                    
            return True, "Build completed successfully"
            
        except Exception as e:
            return False, f"Build failed: {str(e)}"

    def parse_keybinds(self):
        keybinds = []
        if not self.config_files:
            return keybinds

        # Enhanced regex pattern for keybindings
        pattern = r'{\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*(?:{?\.?i?\s*=\s*)?([^}]+)}\s*},'
        
        for file_content in self.config_files.values():
            for match in re.finditer(pattern, file_content):
                mod = match.group(1).strip()
                key = match.group(2).strip()
                func = match.group(3).strip()
                arg = match.group(4).strip()
                
                # Parse SHCMD commands
                if 'SHCMD' in arg:
                    arg = re.search(r'SHCMD\("(.+?)"\)', arg)
                    if arg:
                        arg = arg.group(1)
                
                keybind = {
                    'mod': mod,
                    'key': key,
                    'function': func,
                    'argument': arg
                }
                keybinds.append(keybind)
        
        return keybinds

    def parse_config(self):
        config = {}
        if not self.config_files:
            return config
            
        patterns = [
            (r'#define\s+(\w+)\s+(.+?)(?:/\*.*\*/)?(?:\n|$)', 'define'),
            (r'static\s+(?:const\s+)?(?:unsigned\s+)?int\s+(\w+)\s*=\s*(.+?);', 'int'),
            (r'static\s+const\s+char\s+(\w+)\[\]\s*=\s*"([^"]+)";', 'string'),
        ]
        
        for file_content in self.config_files.values():
            for pattern, type_ in patterns:
                for match in re.finditer(pattern, file_content, re.MULTILINE):
                    key = match.group(1)
                    value = match.group(2).strip()
                    config[key] = {'value': value, 'type': type_}
        
        return config

    def organize_config(self):
        # Appearance settings
        appearance_settings = {
            'borderpx': ('Border Width', 'int'),
            'gappx': ('Gap Size', 'int'),
            'snap': ('Snap Pixels', 'int'),
            'showbar': ('Show Bar', 'bool'),
            'topbar': ('Bar on Top', 'bool'),
            'nmaster': ('Number of Masters', 'int'),
            'resizehints': ('Respect Size Hints', 'bool'),
            'lockfullscreen': ('Lock Fullscreen', 'bool'),
            'focusonwheel': ('Focus on Mouse Wheel', 'bool'),
            'vertpad': ('Vertical Padding', 'int'),
            'sidepad': ('Side Padding', 'int'),
        }
        
        self.categories['Appearance'] = [
            {
                'name': name,
                'key': key,
                'type': type_,
                'value': self.config.get(key, {}).get('value', '0')
            }
            for key, (name, type_) in appearance_settings.items()
        ]

        # Parse keybindings
        self.categories['Keybinds'] = self.parse_keybinds()

class ModernConfigurator(Gtk.Window):
    def __init__(self, config):
        super().__init__(title="DWM Studio")
        self.config = config
        self.set_default_size(1280, 800)
        self.set_resizable(True)
        
        # Create header bar
        self.setup_header_bar()
        
        # Setup UI
        self.setup_style()
        self.setup_ui()
        
        # Connect signals
        self.connect("delete-event", Gtk.main_quit)

    def setup_header_bar(self):
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "DWM Studio"
        
        # Search button
        search_button = Gtk.ToggleButton()
        search_icon = Gio.ThemedIcon(name="edit-find-symbolic")
        search_image = Gtk.Image.new_from_gicon(search_icon, Gtk.IconSize.BUTTON)
        search_button.add(search_image)
        search_button.connect("toggled", self.on_search_toggled)
        header.pack_end(search_button)
        
        # Build button
        build_button = Gtk.Button(label="Build")
        build_button.connect("clicked", self.on_build_clicked)
        header.pack_start(build_button)
        
        self.set_titlebar(header)

    def setup_style(self):
        css = b"""
        /* Arc Browser Dark Theme */
        @define-color bg_color #2f343f;
        @define-color fg_color #d3dae3;
        @define-color selected_bg_color #5294e2;
        @define-color selected_fg_color #ffffff;
        @define-color error_color #cc575d;
        @define-color success_color #68b723;
        @define-color warning_color #f6d32d;
        
        window {
            background-color: @bg_color;
            color: @fg_color;
        }
        
        headerbar {
            background: linear-gradient(to bottom, #353945, #2f343f);
            border-bottom: 1px solid #262b33;
            padding: 6px;
        }
        
        headerbar button {
            background: linear-gradient(to bottom, #404552, #383c4a);
            border: 1px solid #262b33;
            border-radius: 3px;
            color: @fg_color;
            padding: 4px 8px;
        }
        
        headerbar button:hover {
            background: linear-gradient(to bottom, #454c5c, #3d4251);
        }
        
        .search-bar {
            background-color: #383c4a;
            border-bottom: 1px solid #262b33;
            padding: 8px;
        }
        
        .search-entry {
            background-color: #404552;
            color: @fg_color;
            border: 1px solid #2b2e39;
            border-radius: 3px;
            padding: 6px;
        }
        
        .sidebar {
            background-color: #353945;
            border-right: 1px solid #262b33;
        }
        
        .sidebar button {
            background: transparent;
            border: none;
            border-radius: 0;
            color: @fg_color;
            padding: 8px 12px;
            margin: 1px 0;
        }
        
        .sidebar button:hover {
            background-color: alpha(@selected_bg_color, 0.1);
        }
        
        .sidebar button:checked {
            background-color: @selected_bg_color;
            color: @selected_fg_color;
        }
        
        .content-area {
            background-color: #2f343f;
            padding: 16px;
        }
        
        .settings-row {
            padding: 12px;
            border-bottom: 1px solid #262b33;
        }
        
        .settings-row:hover {
            background-color: alpha(@selected_bg_color, 0.1);
        }
        
        entry {
            background-color: #404552;
            color: @fg_color;
            border: 1px solid #2b2e39;
            border-radius: 3px;
            padding: 6px;
        }
        
        switch {
            background-color: #404552;
            border: 1px solid #2b2e39;
            border-radius: 12px;
            min-width: 48px;
            min-height: 24px;
        }
        
        switch:checked {
            background-color: @selected_bg_color;
        }
        
        .keybind-row {
            background-color: #383c4a;
            border-radius: 3px;
            margin: 4px 0;
            padding: 8px;
        }
        
        .keybind-row entry {
            margin: 0 4px;
        }
        
        scrolledwindow {
            border: none;
        }
        
        scrolledwindow undershoot {
            background: none;
        }
        
        scrollbar {
            background-color: transparent;
            border: none;
        }
        
        scrollbar slider {
            background-color: alpha(@fg_color, 0.3);
            border-radius: 6px;
            min-width: 8px;
            min-height: 8px;
        }
        
        scrollbar slider:hover {
            background-color: alpha(@fg_color, 0.5);
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def setup_ui(self):
        # Main container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Search bar (initially hidden)
        self.search_bar = Gtk.SearchBar()
        self.search_bar.get_style_context().add_class('search-bar')
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.get_style_context().add_class('search-entry')
        self.search_entry.connect('search-changed', self.on_search_changed)
        self.search_bar.add(self.search_entry)
        self.main_box.pack_start(self.search_bar, False, False, 0)
        
        # Content area
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        # Sidebar
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.get_style_context().add_class('sidebar')
        sidebar.set_size_request(200, -1)
        
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        # Create sidebar buttons and stack pages
        self.pages = ['General', 'Appearance', 'Keybinds', 'Rules', 'Patches']
        self.page_buttons = {}
        
        for page in self.pages:
            button = Gtk.Button(label=page)
            button.connect('clicked', self.on_page_clicked)
            sidebar.pack_start(button, False, False, 0)
            self.page_buttons[page] = button
            
            # Create stack page
            page_content = self.create_page_content(page)
            self.stack.add_named(page_content, page.lower())
        
        content_box.pack_start(sidebar, False, False, 0)
        
        # Stack container
        stack_container = Gtk.Box()
        stack_container.get_style_context().add_class('content-area')
        stack_container.pack_start(self.stack, True, True, 0)
        
        content_box.pack_start(stack_container, True, True, 0)
        self.main_box.pack_start(content_box, True, True, 0)
        
        self.add(self.main_box)
        self.set_active_page('General')

    def create_page_content(self, page):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        if page == 'General':
            box.pack_start(self.create_general_page(), True, True, 0)
        elif page == 'Appearance':
            box.pack_start(self.create_appearance_page(), True, True, 0)
        elif page == 'Keybinds':
            box.pack_start(self.create_keybinds_page(), True, True, 0)
        elif page == 'Rules':
            box.pack_start(self.create_rules_page(), True, True, 0)
        elif page == 'Patches':
            box.pack_start(self.create_patches_page(), True, True, 0)
            
        scrolled.add(box)
        return scrolled

    def create_general_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        box.set_margin_start(16)
        box.set_margin_end(16)
        
        # DWM Path
        path_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        path_row.get_style_context().add_class('settings-row')
        
        path_label = Gtk.Label(label="DWM Installation Path")
        path_label.set_halign(Gtk.Align.START)
        
        path_entry = Gtk.Entry()
        path_entry.set_text(self.config.dwm_path or "")
        path_entry.set_hexpand(True)
        
        browse_btn = Gtk.Button(label="Browse")
        browse_btn.connect("clicked", self.on_browse_clicked)
        
        path_row.pack_start(path_label, False, False, 0)
        path_row.pack_start(path_entry, True, True, 0)
        path_row.pack_start(browse_btn, False, False, 0)
        
        # Backup section
        backup_frame = Gtk.Frame(label="Backups")
        backup_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        backup_box.set_margin_top(8)
        backup_box.set_margin_bottom(8)
        backup_box.set_margin_start(8)
        backup_box.set_margin_end(8)
        
        backup_btn = Gtk.Button(label="Create Backup")
        backup_btn.connect("clicked", self.on_backup_clicked)
        
        restore_btn = Gtk.Button(label="Restore Backup")
        restore_btn.connect("clicked", self.on_restore_clicked)
        
        backup_box.pack_start(backup_btn, False, False, 0)
        backup_box.pack_start(restore_btn, False, False, 0)
        backup_frame.add(backup_box)
        
        box.pack_start(path_row, False, False, 0)
        box.pack_start(backup_frame, False, False, 0)
        
        return box

    def create_keybinds_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_start(16)
        box.set_margin_end(16)
        
        # Add new keybind button
        add_btn = Gtk.Button(label="Add Keybinding")
        add_btn.connect("clicked", self.on_add_keybind)
        box.pack_start(add_btn, False, False, 0)
        
        # Keybindings list
        for keybind in self.config.categories['Keybinds']:
            row = self.create_keybind_row(keybind)
            box.pack_start(row, False, False, 0)
        
        return box

    def create_keybind_row(self, keybind):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.get_style_context().add_class('keybind-row')
        
        # Modifier entry
        mod_entry = Gtk.Entry()
        mod_entry.set_text(keybind['mod'])
        mod_entry.set_width_chars(15)
        
        # Key entry
        key_entry = Gtk.Entry()
        key_entry.set_text(keybind['key'])
        key_entry.set_width_chars(15)
        
        # Function entry
        func_entry = Gtk.Entry()
        func_entry.set_text(keybind['function'])
        func_entry.set_width_chars(20)
        
        # Argument entry
        arg_entry = Gtk.Entry()
        arg_entry.set_text(keybind['argument'])
        arg_entry.set_hexpand(True)
        
        # Delete button
        delete_btn = Gtk.Button()
        delete_icon = Gio.ThemedIcon(name="edit-delete-symbolic")
        delete_image = Gtk.Image.new_from_gicon(delete_icon, Gtk.IconSize.BUTTON)
        delete_btn.add(delete_image)
        delete_btn.connect("clicked", self.on_delete_keybind, row)
        
        row.pack_start(mod_entry, False, False, 0)
        row.pack_start(key_entry, False, False, 0)
        row.pack_start(func_entry, False, False, 0)
        row.pack_start(arg_entry, True, True, 0)
        row.pack_start(delete_btn, False, False, 0)
        
        return row

    def on_build_clicked(self, button):
        dialog = PasswordDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            password = dialog.get_password()
            dialog.destroy()
            
            success, message = self.config.build_dwm(password)
            self.show_message_dialog(
                "Build Result",
                "Success" if success else "Error",
                message
            )
        else:
            dialog.destroy()

    def show_message_dialog(self, title, header, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=header
        )
        dialog.format_secondary_text(message)
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def on_search_toggled(self, button):
        self.search_bar.set_search_mode(button.get_active())

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
        # Implement search functionality here
        pass

    def on_page_clicked(self, button):
        self.set_active_page(button.get_label())
        self.stack.set_visible_child_name(button.get_label().lower())

    def set_active_page(self, active_page):
        for page, button in self.page_buttons.items():
            if page == active_page:
                button.get_style_context().add_class('active')
            else:
                button.get_style_context().remove_class('active')

    def on_browse_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select DWM Directory",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            # Update DWM path and reload configuration
            pass
        
        dialog.destroy()

class PasswordDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title="Enter Password",
            transient_for=parent,
            flags=0
        )
        
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(300, 100)
        
        box = self.get_content_area()
        box.set_spacing(6)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        
        label = Gtk.Label(label="Enter sudo password:")
        box.add(label)
        
        self.entry = Gtk.Entry()
        self.entry.set_visibility(False)
        self.entry.set_invisible_char("●")
        box.add(self.entry)
        
        self.show_all()

    def get_password(self):
        return self.entry.get_text()

def main():
    config = DWMConfig()
    win = ModernConfigurator(config)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
