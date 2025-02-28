#!/usr/bin/env python3
import os
import re
import json
import threading
import subprocess
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class TerminalOutput(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="Build Output", transient_for=parent)
        self.set_default_size(600, 400)

        self.textview = Gtk.TextView(
            monospace=True,
            editable=False,
            margin=10
        )
        self.buffer = self.textview.get_buffer()

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(self.textview)

        self.add(scrolled)
        self.show_all()

    def append_output(self, text):
        end = self.buffer.get_end_iter()
        self.buffer.insert(end, text)
        self.textview.scroll_to_mark(
            self.buffer.create_mark("end", end, True),
            0, False, 0, 0
        )

class PasswordDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title="Sudo Authentication",
            transient_for=parent,
            flags=0
        )
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "OK", Gtk.ResponseType.OK
        )
        self.set_default_size(300, 100)

        box = self.get_content_area()
        self.password_entry = Gtk.Entry(
            visibility=False,
            activates_default=True
        )
        box.pack_start(Gtk.Label(label="Enter sudo password:"), False, False, 0)
        box.pack_start(self.password_entry, False, False, 0)
        self.show_all()

class SucklessPatcher:
    def __init__(self):
        self.projects = {}
        self.current_filters = {}
        self.backups = {}
        self.config_mk_patterns = {
            'XINERAMA': (r'XINERAMA(LIBS|FLAGS)', '#XINERAMA'),
            'ROUNDED_CORNERS_PATCH': (r'XEXTLIB = -lXext', '#XEXTLIB'),
            'SWALLOW_PATCH': (r'XCBLIBS = -lX11-xcb -lxcb -lxcb-res', '#XCBLIBS'),
            'BAR_WINICON_PATCH': (r'IMLIB2LIBS = -lImlib2', '#IMLIB2LIBS'),
            'BAR_ALPHA_PATCH': (r'XRENDER = -lXrender', '#XRENDER'),
            'BAR_PANGO_PATCH': (r'PANGOINC|PANGOLIB', '#PANGO'),
            'IPC_PATCH': (r'YAJL(LIBS|INC)', '#YAJL')
        }

        self.setup_theme()
        self.detect_projects()
        self.load_backups()
        self.build_gui()

    def detect_projects(self):
        search_paths = [
            os.getcwd(),
            os.path.expanduser("~/suckless"),
            "/usr/local/src"
        ]

        for path in search_paths:
            if os.path.exists(path):
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isdir(full_path):
                        self.load_project(full_path)

    def load_project(self, path):
        def_file = os.path.join(path, 'patches.def.h')
        patch_file = os.path.join(path, 'patches.h')
        config_file = os.path.join(path, 'config.mk')

        if os.path.exists(def_file) and os.path.exists(patch_file):
            project_name = os.path.basename(path)
            self.projects[project_name] = {
                'path': path,
                'patches': self.parse_patches(def_file, patch_file),
                'config': self.parse_config(config_file) if os.path.exists(config_file) else {}
            }

    def parse_config(self, config_file):
        config = {'raw': []}
        with open(config_file, 'r') as f:
            for line in f:
                config['raw'].append(line)
                for patch, (pattern, comment) in self.config_mk_patterns.items():
                    if re.search(pattern, line):
                        config.setdefault(patch, []).append({
                            'line': len(config['raw'])-1,
                            'original': line.strip(),
                            'commented': line.strip().startswith('#')
                        })
        return config

    def update_config_mk(self, project_path, enabled_patches):
        project_name = os.path.basename(project_path)
        project = self.projects[project_name]
        config = project['config']
        new_config = config['raw'].copy()

        for patch_name in enabled_patches:
            if patch_name in self.config_mk_patterns:
                for entry in config.get(patch_name, []):
                    line_num = entry['line']
                    if entry['commented']:
                        new_line = entry['original'].lstrip('#')
                        new_config[line_num] = new_line + '\n'

        with open(os.path.join(project_path, 'config.mk'), 'w') as f:
            f.writelines(new_config)

    def parse_patches(self, def_file, patch_file):
        patches = []
        current_comment = None
        patch_values = {}

        with open(patch_file, 'r') as f:
            for line in f:
                if line.startswith('#define') and '_PATCH' in line:
                    match = re.match(r'#define (\w+)_PATCH (\d+)', line)
                    if match:
                        patch_values[match.group(1)] = int(match.group(2))

        with open(def_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith('/*'):
                    current_comment = {'description': [], 'urls': []}
                    i += 1
                    while i < len(lines) and '*/' not in lines[i]:
                        clean_line = lines[i].strip('/* \n')
                        urls = re.findall(r'https?://[^\s]+', clean_line)
                        current_comment['urls'].extend(urls)
                        current_comment['description'].append(clean_line)
                        i += 1
                    i += 1
                elif line.startswith('#define') and '_PATCH' in line:
                    match = re.match(r'#define (\w+)_PATCH', line)
                    if match:
                        patch_name = match.group(1)
                        patch_data = {
                            'raw_name': patch_name,
                            'name': self.format_name(patch_name),
                            'value': patch_values.get(patch_name, 0)
                        }
                        if current_comment:
                            patch_data.update(current_comment)
                            current_comment = None
                        patches.append(patch_data)
                    i += 1
                else:
                    i += 1
        return patches

    def format_name(self, name):
        return ' '.join(
            word.capitalize()
            for word in name.replace('_PATCH', '').replace('_', ' ').split()
        )

    def load_backups(self):
        for project in self.projects.values():
            backup_dir = os.path.join(project['path'], '.backups')
            self.backups[project['path']] = []
            if os.path.exists(backup_dir):
                self.backups[project['path']] = sorted(
                    [f for f in os.listdir(backup_dir) if f.endswith('.json')],
                    reverse=True
                )

    def create_backup(self, project_path):
        backup_dir = os.path.join(project_path, '.backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"{timestamp}.json")

        config = {}
        with open(os.path.join(project_path, 'patches.h'), 'r') as f:
            for line in f:
                if line.startswith('#define') and '_PATCH' in line:
                    match = re.match(r'#define (\w+)_PATCH (\d+)', line)
                    if match:
                        config[match.group(1)] = int(match.group(2))

        with open(backup_file, 'w') as f:
            json.dump(config, f)

        return backup_file

    def setup_theme(self):
        css = b"""
        * {
            background-color: #2d2d2d;
            color: #ffffff;
        }
        .switch trough {
            background-color: #ff453a;
            border-radius: 15px;
            border: 1px solid #3d3d3d;
            min-width: 51px;
            min-height: 31px;
            transition: all 0.3s ease-in-out;
        }
        .switch:checked trough {
            background-color: #34c759;
            border-color: transparent;
        }
        .switch slider {
            background-color: white;
            border-radius: 13px;
            min-width: 27px;
            min-height: 27px;
            margin: 1px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            transition: margin 0.3s ease-in-out;
        }
        .switch:not(:checked) slider {
            margin-left: 1px;
            margin-right: 23px;
        }
        .switch:checked slider {
            margin-left: 23px;
            margin-right: 1px;
        }
        .backup-item {
            padding: 8px;
            border-bottom: 1px solid #444;
        }
        .backup-item:hover {
            background-color: #3d3d3d;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def build_gui(self):
        self.window = Gtk.Window(title="Suckless Patcher")
        self.window.set_default_size(1280, 768)

        main_paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, width_request=250)

        backup_header = Gtk.Label(label="Backup History", margin=10)
        self.backup_list = Gtk.ListBox()
        self.backup_list.connect("button-press-event", self.on_backup_button_press)
        scrolled_backups = Gtk.ScrolledWindow()
        scrolled_backups.add(self.backup_list)
        sidebar.pack_start(backup_header, False, False, 0)
        sidebar.pack_start(scrolled_backups, True, True, 0)

        main_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.search_entry = Gtk.SearchEntry(placeholder_text="Search patches (regex allowed)...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_changed)
        main_content.pack_start(self.search_entry, False, False, 5)

        self.notebook = Gtk.Notebook()
        self.create_project_tabs()
        main_content.pack_start(self.notebook, True, True, 0)

        btn_box = Gtk.Box(spacing=10, margin=10)
        for btn in [("Save", self.on_save), ("Export", self.on_export), ("Build", self.on_build)]:
            button = Gtk.Button(label=btn[0])
            button.connect("clicked", btn[1])
            btn_box.pack_end(button, False, False, 0)
        main_content.pack_start(btn_box, False, False, 0)

        main_paned.add1(sidebar)
        main_paned.add2(main_content)
        self.window.add(main_paned)
        self.window.connect("destroy", Gtk.main_quit)
        self.populate_backups()

    def on_backup_button_press(self, listbox, event):
        if event.button == 3:  # Right click
            row = listbox.get_row_at_y(int(event.y))
            if row:
                menu = Gtk.Menu()
                delete_item = Gtk.MenuItem(label="Delete Backup")
                delete_item.connect("activate", self.on_delete_backup, row)
                menu.append(delete_item)
                menu.show_all()
                menu.popup(None, None, None, None, event.button, event.time)
                return True
        return False

    def on_delete_backup(self, menu_item, row):
        box = row.get_child()
        label = box.get_children()[0]
        backup_name = label.get_text()

        for project_path in self.backups:
            backup_path = os.path.join(project_path, '.backups', backup_name)
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                    self.load_backups()
                    self.populate_backups()
                    self.show_message(f"Deleted backup: {backup_name}")
                except Exception as e:
                    self.show_message(f"Error deleting backup: {str(e)}", is_error=True)
                break

    def populate_backups(self):
        for child in self.backup_list.get_children():
            self.backup_list.remove(child)

        for project_path, backups in self.backups.items():
            for backup in backups:
                row = Gtk.ListBoxRow()
                box = Gtk.Box(spacing=10)
                label = Gtk.Label(label=os.path.basename(backup))
                restore_btn = Gtk.Button(label="Restore")
                restore_btn.connect("clicked", self.on_restore_backup, project_path, backup)
                box.pack_start(label, True, True, 0)
                box.pack_start(restore_btn, False, False, 0)
                row.add(box)
                self.backup_list.add(row)
        self.backup_list.show_all()

    def create_project_tabs(self):
        for project_name, data in self.projects.items():
            tab = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            scrolled = Gtk.ScrolledWindow()
            patch_list = Gtk.ListBox()
            for patch in data['patches']:
                row = self.create_patch_row(patch)
                patch_list.add(row)
            scrolled.add(patch_list)
            tab.pack_start(scrolled, True, True, 0)
            self.notebook.append_page(tab, Gtk.Label(label=project_name))

    def create_patch_row(self, patch):
        row = Gtk.ListBoxRow()
        expander = Gtk.Expander(label=patch['name'])
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        switch = Gtk.Switch(active=bool(patch['value']))
        switch.connect("state-set", self.on_switch_toggled, patch)
        switch.get_style_context().add_class("switch")

        desc_label = Gtk.Label(
            label="\n".join(patch.get('description', ['No description available'])),
            wrap=True,
            xalign=0
        )

        url_box = Gtk.Box(spacing=5)
        for url in patch.get('urls', []):
            btn = Gtk.LinkButton(uri=url, label=url)
            url_box.pack_start(btn, False, False, 0)

        header_box = Gtk.Box(spacing=10)
        header_box.pack_start(Gtk.Label(label=patch['name'], xalign=0), True, True, 0)
        header_box.pack_end(switch, False, False, 0)

        content_box.pack_start(header_box, False, False, 0)
        content_box.pack_start(desc_label, False, False, 0)
        content_box.pack_start(url_box, False, False, 0)
        expander.add(content_box)
        row.add(expander)
        return row

    def on_switch_toggled(self, switch, state, patch):
        patch['value'] = int(state)

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
        current_tab = self.notebook.get_nth_page(self.notebook.get_current_page())
        scrolled = current_tab.get_children()[0]
        listbox = scrolled.get_child()

        try:
            pattern = re.compile(search_text, re.IGNORECASE)
            use_regex = True
        except re.error:
            use_regex = False

        for row in listbox.get_children():
            if isinstance(row, Gtk.ListBoxRow):
                expander = row.get_child()
                label_text = expander.get_label().lower()
                if use_regex:
                    match = pattern.search(label_text)
                else:
                    match = search_text in label_text
                row.set_visible(match)
                row.set_no_show_all(not match)

    def on_save(self, button):
        current_project = list(self.projects.keys())[self.notebook.get_current_page()]
        project = self.projects[current_project]
        project_path = project['path']

        with open(os.path.join(project_path, 'patches.h'), 'w') as f:
            for patch in project['patches']:
                # Write description as comment
                if 'description' in patch:
                    desc = "\n".join([f"/* {line} */" for line in patch['description']])
                    f.write(f"{desc}\n")
                f.write(f"#define {patch['raw_name']}_PATCH {patch['value']}\n\n")

        enabled_patches = [p['raw_name'] for p in project['patches'] if p['value']]
        self.update_config_mk(project_path, enabled_patches)
        self.create_backup(project_path)
        self.show_message("Configuration saved and backed up!")

    def on_export(self, button):
        enabled_patches = {}
        for project, data in self.projects.items():
            enabled = [p['raw_name'] for p in data['patches'] if p['value']]
            if enabled:
                enabled_patches[project] = enabled

        dialog = Gtk.FileChooserDialog(
            title="Export Patches",
            parent=self.window,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )
        dialog.set_current_name("suckless_patches.json")

        if dialog.run() == Gtk.ResponseType.OK:
            with open(dialog.get_filename(), 'w') as f:
                json.dump(enabled_patches, f, indent=2)
            self.show_message("Patches exported successfully!")
        dialog.destroy()

    def on_build(self, button):
        current_project = list(self.projects.keys())[self.notebook.get_current_page()]
        project_path = self.projects[current_project]['path']

        dialog = PasswordDialog(self.window)
        response = dialog.run()
        password = dialog.password_entry.get_text()
        dialog.destroy()

        if response != Gtk.ResponseType.OK or not password:
            return

        term = TerminalOutput(self.window)

        def run_build():
            nonlocal password
            try:
                process = subprocess.Popen(
                    ['sudo', '-S', 'make', 'clean', 'install'],
                    cwd=project_path,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )

                process.stdin.write(password + '\n')
                process.stdin.flush()

                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    GLib.idle_add(term.append_output, line)

                if process.returncode == 0:
                    GLib.idle_add(term.destroy)  # Close terminal on success
                else:
                    GLib.idle_add(self.show_message,
                        "Build failed! Possible reasons:\n"
                        "1. Incorrect sudo password\n"
                        "2. config.mk requirements not met\n"
                        "3. Missing dependencies",
                        is_error=True)
            except Exception as e:
                GLib.idle_add(self.show_message, f"Error: {str(e)}", is_error=True)
            finally:
                password = None

        threading.Thread(target=run_build, daemon=True).start()

    def on_restore_backup(self, button, project_path, backup_file):
        full_path = os.path.join(project_path, '.backups', backup_file)
        try:
            with open(full_path, 'r') as f:
                backup_config = json.load(f)

            for project in self.projects.values():
                if project['path'] == project_path:
                    for patch in project['patches']:
                        patch['value'] = backup_config.get(patch['raw_name'], 0)
                    break

            self.show_message(f"Restored backup: {backup_file}")
            self.refresh_ui()
        except Exception as e:
            self.show_message(f"Restore failed: {str(e)}", is_error=True)

    def refresh_ui(self):
        self.window.destroy()
        self.__init__()
        self.window.show_all()

    def show_message(self, message, is_error=False):
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR if is_error else Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def run(self):
        self.window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = SucklessPatcher()
    app.run()
