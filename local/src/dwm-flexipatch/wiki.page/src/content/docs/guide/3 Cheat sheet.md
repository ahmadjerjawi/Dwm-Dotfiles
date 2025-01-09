---
title: Key Bindings
---
<div align="center">
    <h1>Cheat Sheet</h1>
</div>

## Introduction
The window manager dwm abstractly orders all of your windows into a stack from most important to least based on when you last manipulated it. dwm is an easy-to-use window manager, but you should understand that it makes use of that stack layout. If you’re not familiar, I recommend searching it up yourself. However, if you want to change any of the “Desktop Environment” things, just press `Mod`+`Shift`+`c`, and it will open dmenu where you can select what file to change and you can save from there. Notice also the case sensitivity of the shortcuts. Be sure you play around with these. Be flexible with the basic commands, and the system will grow on you quick.

### Basic Commands
- `Mod`+`Shift`+`[Capital letter]` (because you need to press shift to capitalize the letters even if caps on)
- `Mod`+`Enter`: Spawn terminal (the default terminal is st; run `man st` for more.)
- `Mod` + `Shift` + `Enter`: Spawn terminal floating scratchpad
- `Mod`+`q`: Close window
- `Mod`+`d`: dmenu (For running commands or programs without shortcuts)
- `Mod`+`j/k`: Cycle through windows by their stack order
- `Mod`+`Shift`+`j/k`: Changes windows postion on the stack
- `Mod`+`Space`: Make selected window the master (or switch master with 2nd)
- `Mod`+`h/l`: Change width of master window
- `Mod`+`z/x`: Increase/decrease gaps (may also hold `Mod` and scroll mouse)
- `Mod`+`a`: Toggle gaps
- `Mod`+`A`: Gaps return to default values (may also hold `Mod` and middle click)
- `Mod`+`Shift`+`Space`: Make a window float (move and resize with `Mod`+left/right click)
- `Mod`+`s`: Make/unmake a window “sticky” (follows you from tag to tag)
- `Mod`+`b`: Toggle status bar (may also middle click on desktop)
- `Mod`+`shift`+`B`: Toggle Bluetooth dmenu (may also use bluetoothctl)

### Window Layouts

- `Mod`+`t`: Tiling mode (active by default)
- `Mod`+`T`: Bottom stack mode (just like tiling, but master is on top)
- `Mod`+`f`: Fullscreen mode
- `Mod`+`F`: Floating (AKA normie) mode
- `Mod`+`y`: Fibonacci spiral mode
- `Mod`+`Y`: Dwindle mode (similar to Fibonacci)
- `Mod`+`u`: Master on the left, other windows in monocle mode
- `Mod`+`U`: Monocle mode (all windows fullscreen and cycle through)
- `Mod`+`i`: Center the master window
- `Mod`+`I`: Center and float the master window
- `Mod`+`o/O`: Increase/decrease the number of master windows

### Basic Programs

- `Mod`+`e`: nemo (file manager)
- `Mod`+`r`: htop (task manager , system monitor that Redditors use to look cool)
- `Mod`+`m`: ncmpcpp (music player)
- `Mod`+`M`: Mutes / Unmute
- `Mod`+`w`: Web browser (chromium)
- `Mod`+`W`: nmtui (for connecting to wireless internet / wifi control )
- `Mod`+`n`: vimwiki ( for notes )
- `Mod`+`F4`: pulsemixer  ( audio system control speakers )
- `Mod`+`Shift`+`Enter`: Show / hide dropdown terminal
- `Mod`+`'`: Show / hide dropdown calculator
- `Mod`+`D`: Runs Dmenu / app launcher

### Tags/Workspaces

There are nine tags, active tags are highlighted in the top left.

- `Mod`+`(Number)`: Go to that number tag
- - `Mod`+`Shift`+`(Number)`: Send window to that tag
- `Mod`+`Tab`: Go to previous tag (may also use `\` for Tab)
- `Mod`+`g`: Go to left tag (hold shift to send window there)
- `Mod`+`;`: Go to right tag (hold shift to send window there)
- `Mod`+`Left/Right`: Go to another display
- `Mod`+`Shift`+`Left/+Right`: Move window to another display

### System

- `Mod`+`BackSpace`: Choose to lock screen, logout, shutdown, reboot, etc.
- `Mod`+`F1`: Show this document
- `Mod`+`F3`: Select screen/display to use
- `Mod`+`F4`: pulsemixer (audio control)
- `Mod`+`F6`: Transmission torrent client (not installed by default)
- `Mod`+`F7`: Toggle on/off transmission client via dmenu
- `Mod`+`F9`: Mount a USB drive/hard drive or Android
- `Mod`+`F10`: Unmount a non-essential drive or Android
- `Mod`+`F11`: View webcam
- `Mod`+`F12`: Rerun keyboard mapping scripts if new keyboard is attached
- `Mod`+`'`: Select an emoji to clipboard
- `Mod`+`Insert`: Paste text you have saved in a file at `~`
- `Alt`+`Shift`: Changes keyboard layout using cycle-keyboard script at Chnages Language `~/.local/bin/cycle-keyboard`
- `Mod` + `Shift` + `V` to shows clipmenu dmenu
- `Mod` + `Shift` + `C` to shows configes of the suckless apps (dwm , dmenu , dwmblocks ..etc) located at `~/.local/src`
- `Mod` + `Shift` + `R` to renew / rest dwm session without saving the apps postions to apply changes on the source code
### Audio

I use ncmpcpp as a music player, which is a front end for mpd.

- `Mod`+`m`: ncmpcpp, the music player
- `Mod`+`.`: Next track
- `Mod`+`,`: Previous track
- `Mod`+`<`: Restart track
- `Mod`+`>`: Toggle playlist looping
- `Mod`+`p`: Toggle pause
- `Mod`+`p`: Force pause music player daemon and all mpv videos
- `Mod`+`M`: Mute all audio
- `Mod`+`-`: Decrease volume (holding shift increases amount)
- `Mod`+`+`: Increase volume (holding shift increases amount)
- `Mod`+`[` (Back 10 seconds; holding shift moves by one minute)
- `Mod`+`]` (Forward 10 seconds; holding shift moves by one minute)
- `Mod`+`F4`: pulsemixer (general audio/volume sink/source control)

### Recording

I use maim and ffmpeg to make different recordings of the desktop and audio. All of these recording shortcuts will output into `˜`, and will not overwrite previous recordings as their names are based on their exact times.

- `PrintScreen`: Take a screenshot
- `Shift`+`PrintScreen`: Select area to screenshot
- `Mod`+`PrintScreen`: Opens dmenu menu to select kind of audio/video recording
- `Mod`+`Delete`: Kills any recording started in the above way.
- `Mod`+`Shift`+`C`: Toggles a webcam in the bottom right for screencasting.
- `Mod`+`ScrollLock`: Toggle  screenkey (if installed) to show keypresses
