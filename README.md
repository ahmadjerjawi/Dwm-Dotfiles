
# Dwm Dotfiles
![36789ebb-ee94-44c3-b7c7-3b2d48c614b2(2)](https://github.com/user-attachments/assets/743e8a7f-105b-4d10-b3de-351d8b889f3c)




# My dwm-flexipatch fork and other app

This is a customized version of dwm-flexipatch with added functionality for dwmblocks, additional scripts, files, icons, and fontsp.
[My wiki for the system](https://ahmadjerjawi.github.io/wiki/)

## Things  I Did
- Nemo file manager
- St my terminal
- dmenu is i can say so much things
- dwmblocks as my status bar
and i am planning to add webage using surf to act as a config manager without the need of so complex one
- dwm supports rtl languages but not St
- new history atuin instead of the just shell history you need to setup it
- fzf for file fidning in terminal 

## Features

- Integration with dwmblocks for dynamic status bar
- Custom scripts for enhanced system management and productivity
- Additional files for personalization and convenience
- Included icons and fonts to enrich the user interface
![pic-full-250314-1134-38](https://github.com/user-attachments/assets/56dcfba8-79ac-4cc9-ba4b-dd1e8daecc86)
![pic-full-250228-1113-03](https://github.com/user-attachments/assets/b08ebcd4-4143-4c73-b27a-366738a6beac)


## Patches 
### **Bar Patches**
- `BAR_DWMBLOCKS_PATCH`: Integrate dwmblocks status bar.
- `BAR_DWMBLOCKS_SIGUSR1_PATCH`: Enable SIGUSR1 for dwmblocks.
- `BAR_LAYOUTMENU_PATCH`: Add layout selection menu.
- `BAR_LTSYMBOL_PATCH`: Display layout symbol in bar.
- `BAR_STATUS_PATCH`: Basic status bar support.
- `BAR_STATUSCMD_PATCH`: Execute commands from status bar.
- `BAR_STATUS2D_PATCH`: Enhanced status bar with colors.
- `BAR_SYSTRAY_PATCH`: Add system tray to bar.
- `BAR_TAGS_PATCH`: Display workspace tags in bar.
- `BAR_UNDERLINETAGS_PATCH`: Underline active tags.
- `BAR_WINICON_PATCH`: Show window icons in bar.
- `BAR_WINTITLE_PATCH`: Display window title in bar.
- `BAR_WINTITLE_FLOATING_PATCH`: Show floating window titles.
- `BAR_ALPHA_PATCH`: Transparency support for bar.
- `BAR_HIDEVACANTTAGS_PATCH`: Hide empty workspace tags.
- `BAR_PADDING_VANITYGAPS_PATCH`: Apply padding for vanity gaps.
- `BAR_STATUSPADDING_PATCH`: Adjust padding for status bar.

### **Window Management Patches**
- `ALT_TAB_PATCH`: Enable alt-tab window switching.
- `ALWAYSCENTER_PATCH`: Center new windows by default.
- `ASPECTRESIZE_PATCH`: Maintain aspect ratio on resize.
- `BIDI_PATCH`: Support bidirectional text.
- `COOL_AUTOSTART_PATCH`: Auto-launch programs on startup.
- `CYCLELAYOUTS_PATCH`: Cycle through available layouts.
- `FULLSCREEN_PATCH`: Fullscreen window support.
- `MOVESTACK_PATCH`: Move windows within stack.
- `PERTAG_PATCH`: Separate settings per workspace.
- `RENAMED_SCRATCHPADS_PATCH`: Named scratchpads for quick access.
- `RESIZEPOINT_PATCH`: Resize windows from any corner.
- `RESTARTSIG_PATCH`: Restart dwm with a signal.
- `ROUNDED_CORNERS_PATCH`: Rounded window corners.
- `SAVEFLOATS_PATCH`: Remember floating window positions.
- `SEAMLESS_RESTART_PATCH`: Keep state on restart.
- `SHIFTSWAPTAGS_PATCH`: Swap tags with a shift key.
- `SHIFTTAG_PATCH`: Move windows between tags.
- `SHIFTTAGCLIENTS_PATCH`: Shift all clients to a tag.
- `SHIFTVIEW_PATCH`: Shift view between workspaces.
- `STACKER_PATCH`: Improved window stacking.
- `STICKY_PATCH`: Make windows sticky (always visible).
- `SWALLOW_PATCH`: Embed child windows into parents.
- `TOGGLEFULLSCREEN_PATCH`: Toggle fullscreen state.
- `VANITYGAPS_PATCH`: Add gaps between windows.
- `WINDOWROLERULE_PATCH`: Apply rules based on window roles.

### **Layout Patches**
- `FLEXTILE_DELUXE_LAYOUT`: Advanced tiling layout options.
- `TILE_LAYOUT`: Default tiling window layout.
- `MONOCLE_LAYOUT`: Single window maximized layout.

## Shortucts and keybinds 
 stored at the guide by Reading the f config at dwm-flexipatch
 and if you need to add change and if i forgot just read the source code and you know what you are doing Or just press Super + F1
 to see the [wiki](https://ahmadjerjawi.github.io/wiki/)
## Getting Started

To use this repository, follow these steps:
make sure to have yay installed or you do the work manually

1. Clone this repsotery
```bash
git clone "https://github.com/ahmadjerjawi/Dwm-Dotfiles.git"
```
the apps that removed in the changes scirpt will remove them
2. Run install.sh
```bash
sudo -e install.sh
```
3. Restart / Renew Dwm
```bash
   reboot
```

## Note 
If you want to change the keybindings you should also change the keybindings in the scripts becuase they also uses the same binings becuase i didnt know how to implement scatching pads into dwmblocks so i used xdotools to emulate the key pressing


