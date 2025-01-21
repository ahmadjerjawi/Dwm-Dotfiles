---
title: Introduction
---
## Welcome!
My Documentation For This System

by **Ahmad Jerjawi**

If you are using This wiki locally not from the wiki
Use arrow keys to navigate this document. Pressing **F11** will fit it to window width. **Ctrl + Shift + j/k** zoom in and out. **Mod+f** to toggle fullscreen. **Mod+q** to quit. **/** to search for text. (These are general binds set for surf, the web browser)

- **Mod+F1** will show this document at any time.
- By Mod, I mean the Super Key, usually known as “the Windows Key.”
- FAQs are at the end of this document.


### Philosophy
At dwm, simplicity, clarity, and frugality reign supreme. We believe in straightforward, understandable software that enhances usability. In a world filled with complexity, we champion simplicity for a superior computing experience.

### Ideology
In dwm, keyboard shortcuts take precedence over graphical menus. Speed, efficiency, and logic drive this choice. Whether logging out or capturing screenshots, keystrokes like `Print` or `Super` + `Shift` + `q` expedite tasks without menu navigation.

### Why Choose dwm?
dwm offers not only speed and efficiency but also a community committed to simplicity and usability. Embrace dwm, and discover heightened productivity through streamlined computing.

### Basic goals and principles of this system
- **Naturalness** – Remove the border between mind and matter: everything important should be as few keypresses as possible away from you, and you shouldn’t have to think about what you’re doing. Immersion.
- **Economy** – Programs should be simple and light on system resources and highly extensible. Because of this, many are terminal or small ncurses programs that have all the magic inside of them.
- **Keyboard/vim-centrality** – All terminal programs (and other programs) use vim keys when possible. Your hands never need leave the home row or thereabout.
- **Decentralization** – This system is a web of small, modifiable and replaceable programs that users can easily customize.

### General keyboard changes
- The menu button (usually between the right Alt and Ctrl) is an alternative Super/Mod button. This is to make one-handing on laptops easier.
- If you’d like to change any of these keyboard changes, you need only open and change the remaps script. All custom scripts are located in `~/.local/bin/`. Actually, this should go without saying, but everything here can easily be changed. Below in this document, there is information about where to change programs/components.
- Additionally, while this isn’t a part of the desktop environment, the default editing mode in the shell is using vi bindings. If you want to learn more of this, search it yourself. This setting can be changed if you don’t like it by deleting or commenting out the contents of `~/.config/shell/inputrc`.
- To change the Keyboard layout press **Shift + Alt** and you can also to change the keyboard layouts (Add/Remove) to do this vim it from `~/.local/bin/cycle-keyboard`


:::note[Note for changing keybinding]
If you want to change the keybindings, you should also change the keybindings in the scripts because they also use the same bindings. I didn't know how to implement scratching pads into dwmblocks, so I used xdotools to emulate the key pressing.
