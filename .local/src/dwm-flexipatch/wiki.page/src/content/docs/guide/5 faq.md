---
title: FAQs
description: This is a page in my Starlight-powered site
---
 # Frequently Asked Questions (FAQs)
Here are some Questions i got asked when i am using my system around the internet and in real life and my answers that may not satasfie you


## How do I copy and paste?

Copying and pasting is always program-specific on any system. In most graphical programs, copy and paste will be the same as they are on Windows: ctrl-c and ctrl-v. In the Linux terminal, those binds have other more important purposes, so you can run `man st` to see how to copy and paste in the terminal build.

Additionally, I've set vim to use the clipboard as the default buffer, which means when you yank or delete something in vim, it will be in your system clipboard as well, so you can ctrl-v it into your browser instance, etc. You can also paste material copied from other programs into vim with the typical vim bindings.

## How do I change the background/wallpaper?

The system will always read the file `~/.local/share/bg` as the wallpaper. The script `setbg`, if run on an image will set it as the persistent background. When using the file manager, you can simply hover over an image name and right click and click set as wallpaper and this will run `setbg`.

## How do I change the colorscheme?

The system no longer deploys Xresources by default, but check `~/.config/x11/xresources` for a list of color schemes you can activate or add your own. When you save the file, vim will automatically update the colorscheme. If you'd like these colors activated by default on login, there is a line in `~/.config/x11/xprofile` you can uncomment to allow that.

Alternatively, if you want to use `wal` to automatically generate colorschemes from your wallpapers, just install it and `setbg` will automatically detect and run it on startup and wallpaper change.

## How do I set up my email?

Just use your browser or set it up yourself, I don't use email!

## How do I set up my music?

By default, `mpd`, the music daemon assumes that `~/Music` is your music directory. This can be changed in `~/.config/mpd/mpd.conf`. When you add music to your music folder, you may have to run `mpc up` in the terminal to update the database. `mpd` is controlled by `ncmpcpp`, which is accessible by `Mod+m`.

## My Links

You can follow links via the keyboard in this PDF reader by pressing `f` followed by the number that appears on the desired link.

- [My Github Page](https://github.com/ahmadjerjawi) - For the dotfiles you are using/modifying.
