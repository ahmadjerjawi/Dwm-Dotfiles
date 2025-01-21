---
title: Configuration Guide
---

## Configuration

Dotfiles/settings files for various programs are typically located in `~/.config/`. However, some programs like dwm (the window manager), st (the terminal), and dmenu, among others from the Suckless project, do not have traditional config files. Instead, their source code is located in `~/.local/src/`.

### Suckless Programs Configuration

To configure Suckless programs like dwm, st, and dmenu:

1. **Locate Source Code**: Navigate to `~/.local/src/` (you can use the `rr` command to jump to this directory).

2. **Edit Configurations**: Use the `dmenu_configer` script to start configuring. Press `Mod`+`Shift`+`C` to launch the configuration menu. Here, you can modify the `config.h` files or other relevant source code files according to your preferences.

3. **Reinstall**: After making changes, run `sudo make install` to reinstall the program. Vim is set to automatically recompile and install these programs whenever you save changes to any `config.h` file but not all becuase if you broke your system have time before facing it. Compilation will be nearly instantaneous. You’ll have to restart the program to see its effects, obviously. `Mod`+`Shift`+`r` to renew dwm session and will not save your windows locations obviously
:::caution
**You may Harm your system if you dont know what are you doing or configuired something wrong dont come in and report without troubleshooting**
:::
