#!/bin/bash

# Check if script is running as sudo
if [ "$EUID" -ne 0 ]; then
    echo "Please run as sudo"
    exit 1
fi

# Detect distribution and package manager
if [ -f "/etc/os-release" ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "Cannot detect distribution. Creating generic instructions."
    DISTRO="unknown"
fi

# Check for Arch-based systems and package managers
is_arch_based=0
if [ -x "$(command -v pacman)" ]; then
    is_arch_based=1
    echo "Detected pacman package manager"
    pkg_manager="pacman"
    install_cmd="pacman --noconfirm -S"
elif [ -x "$(command -v yay)" ]; then
    is_arch_based=1
    echo "Detected yay AUR helper"
    pkg_manager="yay"
    install_cmd="yay --noconfirm -S"
elif [ -x "$(command -v paru)" ]; then
    is_arch_based=1
    echo "Detected paru AUR helper"
    pkg_manager="paru"
    install_cmd="paru --noconfirm -S"
fi

# Define packages
PACKAGES=(
    # Core System
    base-devel
    linux-firmware
    linux-headers
    grub
    efibootmgr
    xorg-server
    xorg-xinit
    xorg-xrandr
    xorg-xsetroot 
    xorg-xauth
    xorg-xbacklight
    xorg-xev
    xorg-xinput
    xorg-xkbcomp 
    xorg-xmodmap
    xorg-xrdb
    xwallpaper
    dunst
    tint2
    nemo
    nemo-fileroller
    lxappearance
    arandr
    slock
    pipewire-pulse
    pamixer
    pulsemixer
    wireplumber
    git
    python-pip
    python-pipx
    go
    ocaml
    ocaml-findlib
    ttf-dejavu
    ttf-font-awesome
    ttf-nerd-fonts-symbols
    noto-fonts
    noto-fonts-cjk
    noto-fonts-emoji
    libertinus-font
    papirus-icon-theme
    networkmanager
    network-manager-applet
    neovim
    vim
    bat
    fzf
    maim
    atuin
    dust
    unzip
    zsh
    mpv
    mpd
    mpc
    ffmpeg
    ffmpegthumbnailer
    zathura
    zathura-pdf-mupdf
)

if [ $is_arch_based -eq 1 ]; then
    echo "Installing packages using $pkg_manager..."
    $install_cmd "${PACKAGES[@]}" || {
        echo "Package installation failed. Please check the error messages above."
        exit 1
    }
else
    # Create raw package list
    printf "%s\n" "${PACKAGES[@]}" > "requirements.txt"
    
    # Create instructions file
    cat > "INSTRUCTIONS.txt" << 'EOF'
Installation Instructions
========================

1. Install Required Packages
---------------------------
- Install all packages listed in requirements.txt using your distribution's package manager
  For example:
  - For Debian/Ubuntu: sudo apt install [package-name]
  - For Fedora: sudo dnf install [package-name]
  - For OpenSUSE: sudo zypper install [package-name]

2. Set Up Directory Structure
---------------------------
mkdir -p ~/.local/bin ~/.local/share ~/.local/src ~/.config

3. Copy Configuration Files
--------------------------
cp -r ./local/* ~/.local/
cp -r ./config/* ~/.config/

4. Build and Install Suckless Tools
----------------------------------
cd ~/.local/src/dwm-flexipatch && sudo make clean install
cd ~/.local/src/dwmblocks && sudo make clean install
cd ~/.local/src/dmenu-flexipatch && sudo make clean install
cd ~/.local/src/st && sudo make clean install

5. Set ZSH as Default Shell
--------------------------
chsh -s $(which zsh)

6. Start X Server
----------------
- Add "exec dwm" to your ~/.xinitrc
- Start X with "startx"

7. Additional Setup
------------------
- Configure networkmanager: sudo systemctl enable NetworkManager
- Configure audio: systemctl --user enable pipewire-pulse
- Log out and log back in to ensure all changes take effect

Note: Package names might vary between distributions. You may need to search
for equivalent packages using your distribution's package manager.
EOF
    echo "Created requirements.txt and INSTRUCTIONS.txt files."
fi

# Create necessary directories
echo "Creating directories..."
sudo -u "$SUDO_USER" mkdir -p "$HOME/.local/bin" "$HOME/.local/share" "$HOME/.local/src"

# Copy local files structure if they exist
if [ -d "./local" ]; then
    echo "Copying local files..."
    cp -r ./local/bin/* "$HOME/.local/bin/" 2>/dev/null || true
    cp -r ./local/share/* "$HOME/.local/share/" 2>/dev/null || true
    cp -r ./local/src/* "$HOME/.local/src/" 2>/dev/null || true
fi

# Set correct ownership
chown -R "$SUDO_USER:$SUDO_USER" "$HOME/.local"

# Build and install suckless tools
SUCKLESS_TOOLS=("dwm-flexipatch" "dwmblocks" "dmenu-flexipatch" "st")

for prog in "${SUCKLESS_TOOLS[@]}"; do
    if [ -d "$HOME/.local/src/$prog" ]; then
        echo "Building $prog..."
        cd "$HOME/.local/src/$prog" || continue
        sudo -u "$SUDO_USER" make clean install
    else
        echo "Warning: $prog source not found in ~/.local/src/$prog"
    fi
done

# Change default shell to zsh
if command -v zsh >/dev/null 2>&1; then
    echo "Changing default shell to zsh..."
    chsh -s "$(command -v zsh)" "$SUDO_USER"
else
    echo "Warning: zsh not found. Please install it manually."
fi

echo "Installation completed!"
if [ $is_arch_based -eq 0 ]; then
    echo "Please check INSTRUCTIONS.txt for installation steps and requirements.txt for required packages."
fi
