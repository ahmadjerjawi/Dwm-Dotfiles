---
title: Displays Guide
---

<div align="center">
    <h1>HiDPI and 4K Displays Guide</h1>
</div>

## Introduction
If you have a screen with a very high dots-per-inch (DPI), the interface, particularly the status bar at the top, may appear very small. This guide will help you adjust the display settings to make the interface more comfortable to use.

## Adjusting DPI
To change the DPI (dots-per-inch) of your display, you can use the `xrandr` command. Open a terminal and run the following command, replacing `96` with your desired DPI value:

```bash
xrandr --dpi 96
```

After running the command, you may need to refresh the window manager. You can do this by pressing `Super` + `Shift` + `R`.

### Making DPI Changes Persistent
To make the DPI changes persistent after reboot, you can edit the `~/.xprofile` file. Open the file in a text editor and locate the command similar to the one you used to adjust the DPI. Modify the DPI value as needed and save the file.

## Display Configuration
For a more advanced display configuration, you can use the `displayselect` script. This script provides a user interface for detecting and selecting all connected displays. It allows you to configure multi-monitor setups and adjust display arrangements easily.

### Displayselect Script

```bash
displayselect
```

load the script to a file named `displayselect` in a directory included in your system

This script will provide you with options to configure your display setup conveniently.

Remember to run the script without closing the terminal window to execute it successfully. Or by pressing `Mod`+`F3`
- `Mod`+`Left/Right` – Go to another display
- `Mod`+`Shift`+`Left/+Right` – Move window to another display
- `Mod`+`Shift`/`+-`: Changes screen brightness
