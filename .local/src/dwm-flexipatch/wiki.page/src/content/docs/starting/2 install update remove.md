---
title: Install / Update / Uninstall
---

## Installing
### Before you start
1. This only provides **user-level customization**. You have to set up network, bluetooth, GPU (esp. Nvidia) stuff, etc. yourself but when they are configiured the system will figuire it out by it self
2. You can change the apps it will install from the script or the `progc.csv` and you can change what ever you want
### Automated installation (for Arch distros only)
- _**This is the recommended method**_

Just run the following command.
```bash
git clone "https://raw.githubusercontent.com/ahmadjerjawi/Dotfiles-Dwm-envirmoent/main/install.sh" && sudo ./install.sh
```

### For NixOS
- Currently, these dotfiles are not (yet?)
### Manual installation (basically any distro)
:::note[Note for non-Arch distros]
You'll have to figure out the equivalents of packages inside `progs.csv` later when you install the dependencies.
- To get info of a package (e.g. what executable(s) it provides), search it on [Arch Linux Packages](https://archlinux.org/packages) or the [AUR](https://aur.archlinux.org/packages).
- If you've successfully finished installation on some non-Arch(-based) Linux distro, you're very welcomed to share the package list (also other steps if needed), and we could automate the installation for it in the future. Thanks!
:::
</Steps>

1. Clone the repo
  ```bash
  git clone "https://github.com/ahmadjerjawi/Dotfiles-Dwm-envirmoent/"
  ```
2. Get packages: Install all packages listed inside `progs.csv`. For Arch Linux, just use an AUR helper such as `yay`.

3. Add user to `video` and `input` group
  ```bash
 sudo usermod -aG video,input "$(whoami)" # if this somehow doesn't work, just replace "$(whoami)" with your username
  ```
4. Copy `.config`, `.local` to your home folder (review before doing this or you might have your own config files undesirably overwritten)

- Get started with these keybinds
  - `Super`+`Enter` to start new terminal
  - `Super`+`w` to start your web browser
  - `Super`+`F1` to show this doc which contains all the keybindings

## Updating
### Automatically Update
- `cd` to the repo directory
- Run `git pull` to fetch the latest changes.
- Run `./install.sh` again
:::caution
This will overwrite your files under its target path if it's not inside of the original dotfiles if you have custom scripts or anything that was changed from the one like changed configs Use the [Manual Method](#manually-update)
:::

### Manually Update
```bash
git clone "https://github.com/ahmadjerjawi/Dotfiles-Dwm-envirmoent"
```
- `cd` to the repo directory
- Run `git pull` to fetch the latest changes.
- Grab files you want. Typically you may want to grab the `.config` folder and the `.local`. `.zprofile` , `.zshrc`
- and you are done

## Uninstalling
- Manual uninstallation is **The only option for you**
- Currently, there isn't a script for uninstallation, and it's not going to
- Here goes a long explanation if you care:

> The point is that this repo is not a typical "software", but a set of config,
> Therefore it's very hard to make a proper uninstallation script,
> which should revert all changes made by the installation script.
>
> For example, the installation script will install `yay` (AUR-helper) for you if you don't have one.
> However, what should the uninstallation script do to revert this changes?
> - Remove `yay` or `yay-bin`? Not proper, because you may already have one of them installed by yourself (NOT by the installation script).
> - Even if the installation script had logged the package list installed by the script, it's still not proper to remove `yay` or `yay-bin` when the log showed `yay` or `yay-bin` is installed by the script, because the script can't log its future, and you may have reinstalled `yay` or `yay-bin` another day after the installation script finished, thus they are actually not installed by installation script anymore.
>
> In conclusion, it's nearly not possible to write a proper uninstallation script.
> You'd better make reverted changes manually as you need.
