#!/bin/bash

# Improved DWM Dotfiles Installer Script
# Version: 1.1

### VARIABLES ###
REPO_DIR=$(pwd)
BACKUP_DIR="$HOME/.dotfiles-backup-$(date +%Y%m%d%H%M%S)"
RESTORE_SCRIPT="$HOME/.dotfiles-restore.sh"
LOG_FILE="/tmp/dotfiles-install-$(date +%Y%m%d%H%M%S).log"
AURHELPER="yay"

### FUNCTIONS ###

# Echo with timestamp
log_msg() {
    local timestamp=$(date "+%H:%M:%S")
    echo "[$timestamp] $1"
}

# Check if running on Arch-based system
check_arch_system() {
    log_msg "Checking system compatibility..."
    if ! command -v pacman >/dev/null 2>&1; then
        echo "Error: This script requires an Arch-based system with pacman."
        echo "Your system is not supported."
        exit 1
    fi
    log_msg "✓ System is Arch-based. Proceeding..."
}

# Check and install dependencies
check_dependencies() {
    log_msg "Checking dependencies..."
    if ! command -v whiptail >/dev/null 2>&1; then
        log_msg "Installing whiptail..."
        sudo pacman --noconfirm --needed -Sy libnewt >/dev/null 2>&1 || {
            echo "Error: Failed to install whiptail. Are you running as a user with sudo privileges?"
            exit 1
        }
    fi
    log_msg "✓ Dependencies satisfied."
}

# Display welcome message
welcome_message() {
    whiptail --title "Welcome!" \
        --msgbox "Welcome to DWM Dotfiles Installer!\n\nThis script will:\n1. Install packages from progs.csv\n2. Back up your existing configs\n3. Install DWM and related programs\n4. Create a restore script for reverting changes\n\nThe script requires sudo privileges." 15 65 || {
        log_msg "Installation cancelled by user."
        exit 1
    }
}

# Confirm installation
confirm_installation() {
    whiptail --title "Ready to Install" --yes-button "Let's go!" \
        --no-button "Cancel" \
        --yesno "The installation will now begin.\n\nYour existing .config and .local directories will be backed up to:\n$BACKUP_DIR\n\nA restore script will be created at:\n$RESTORE_SCRIPT" 15 65 || {
        log_msg "Installation cancelled by user."
        exit 1
    }
}

# Create backup of user files
create_backup() {
    log_msg "Creating backup of your configuration files..."

    mkdir -p "$BACKUP_DIR"

    # Backup .config if it exists
    if [ -d "$HOME/.config" ]; then
        mkdir -p "$BACKUP_DIR/.config"
        for dir in $(find "$REPO_DIR/.config" -maxdepth 1 -mindepth 1 -type d -not -path "*/\.*" -printf "%f\n" 2>/dev/null); do
            if [ -d "$HOME/.config/$dir" ]; then
                log_msg "Backing up .config/$dir"
                cp -a "$HOME/.config/$dir" "$BACKUP_DIR/.config/" 2>/dev/null
            fi
        done
        for file in $(find "$REPO_DIR/.config" -maxdepth 1 -mindepth 1 -type f -not -path "*/\.*" -printf "%f\n" 2>/dev/null); do
            if [ -f "$HOME/.config/$file" ]; then
                log_msg "Backing up .config/$file"
                cp -a "$HOME/.config/$file" "$BACKUP_DIR/.config/" 2>/dev/null
            fi
        done
    fi

    # Backup .local if it exists
    if [ -d "$HOME/.local" ]; then
        mkdir -p "$BACKUP_DIR/.local"
        for dir in $(find "$REPO_DIR/.local" -maxdepth 1 -mindepth 1 -type d -not -path "*/\.*" -printf "%f\n" 2>/dev/null); do
            if [ -d "$HOME/.local/$dir" ] && [ "$dir" != "src" ]; then
                log_msg "Backing up .local/$dir"
                cp -a "$HOME/.local/$dir" "$BACKUP_DIR/.local/" 2>/dev/null
            elif [ "$dir" = "src" ]; then
                mkdir -p "$BACKUP_DIR/.local/src"
                for srcdir in $(find "$REPO_DIR/.local/src" -maxdepth 1 -mindepth 1 -type d -printf "%f\n" 2>/dev/null); do
                    if [ -d "$HOME/.local/src/$srcdir" ]; then
                        log_msg "Backing up .local/src/$srcdir"
                        cp -a "$HOME/.local/src/$srcdir" "$BACKUP_DIR/.local/src/" 2>/dev/null
                    fi
                done
            fi
        done
        for file in $(find "$REPO_DIR/.local" -maxdepth 1 -mindepth 1 -type f -not -path "*/\.*" -printf "%f\n" 2>/dev/null); do
            if [ -f "$HOME/.local/$file" ]; then
                log_msg "Backing up .local/$file"
                cp -a "$HOME/.local/$file" "$BACKUP_DIR/.local/" 2>/dev/null
            fi
        done
    fi

    # Backup shell files
    for file in .zprofile .bashrc .zshrc; do
        if [ -f "$HOME/$file" ] && [ -f "$REPO_DIR/$file" ]; then
            log_msg "Backing up $file"
            cp -a "$HOME/$file" "$BACKUP_DIR/" 2>/dev/null
        fi
    done

    log_msg "✓ Backup completed"
}

# Create restore script
create_restore_script() {
    log_msg "Creating restore script..."

    cat > "$RESTORE_SCRIPT" << EOL
#!/bin/bash
# Restore script for DWM Dotfiles
# Created: $(date)

BACKUP_DIR="$BACKUP_DIR"

if [ ! -d "\$BACKUP_DIR" ]; then
    echo "Error: Backup directory not found at \$BACKUP_DIR"
    exit 1
fi

echo "Restoring configuration files from \$BACKUP_DIR..."

# Restore .config
if [ -d "\$BACKUP_DIR/.config" ]; then
    for item in "\$BACKUP_DIR/.config"/*; do
        name=\$(basename "\$item")
        echo "Restoring .config/\$name"
        rm -rf "\$HOME/.config/\$name"
        cp -a "\$item" "\$HOME/.config/"
    done
fi

# Restore .local
if [ -d "\$BACKUP_DIR/.local" ]; then
    for item in "\$BACKUP_DIR/.local"/*; do
        name=\$(basename "\$item")
        if [ "\$name" != "src" ]; then
            echo "Restoring .local/\$name"
            rm -rf "\$HOME/.local/\$name"
            cp -a "\$item" "\$HOME/.local/"
        else
            # Handle src directory specially
            for srcitem in "\$BACKUP_DIR/.local/src"/*; do
                srcname=\$(basename "\$srcitem")
                echo "Restoring .local/src/\$srcname"
                rm -rf "\$HOME/.local/src/\$srcname"
                cp -a "\$srcitem" "\$HOME/.local/src/"
            done
        fi
    done
fi

# Restore shell files
for file in .zprofile .bashrc .zshrc; do
    if [ -f "\$BACKUP_DIR/\$file" ]; then
        echo "Restoring \$file"
        cp -f "\$BACKUP_DIR/\$file" "\$HOME/"
    fi
done

echo "Restoration complete!"
EOL

    chmod +x "$RESTORE_SCRIPT"
    log_msg "✓ Restore script created at $RESTORE_SCRIPT"
}

# Install AUR helper
install_aur_helper() {
    if ! command -v "$AURHELPER" >/dev/null 2>&1; then
        log_msg "Installing AUR helper ($AURHELPER)..."

        # Install git if not already installed
        log_msg "Checking git installation..."
        sudo pacman --noconfirm --needed -S git >/dev/null 2>&1 || return 1

        # Create temporary directory for AUR helper installation
        local tmpdir=$(mktemp -d)
        cd "$tmpdir" || return 1

        log_msg "Cloning $AURHELPER repository..."
        git clone "https://aur.archlinux.org/$AURHELPER.git" >/dev/null 2>&1 || return 1
        cd "$AURHELPER" || return 1

        log_msg "Building and installing $AURHELPER..."
        makepkg --noconfirm -si >/dev/null 2>&1 || return 1

        # Return to original directory
        cd "$REPO_DIR" || return 1
        rm -rf "$tmpdir"
        log_msg "✓ $AURHELPER installed"
    else
        log_msg "✓ $AURHELPER already installed"
    fi
}

# Install packages
install_packages() {
    if [ ! -f "$REPO_DIR/progs.csv" ]; then
        log_msg "Error: progs.csv not found in the repository directory."
        whiptail --msgbox "Error: progs.csv not found in the repository directory." 10 60
        return 1
    fi

    log_msg "Reading package list from progs.csv..."

    # Count total number of packages
    total=$(grep -v "^#" "$REPO_DIR/progs.csv" | wc -l)
    counter=0

    log_msg "Found $total packages to install"

    # Process packages
    while IFS=, read -r tag program comment || [ -n "$tag" ]; do
        # Skip comments and empty lines
        [[ "$tag" =~ ^# ]] && continue
        [ -z "$tag" ] && continue

        counter=$((counter + 1))

        # Remove quotes from comment if present
        comment=$(echo "$comment" | sed -E 's/^"(.*)"$/\1/')

        case "$tag" in
            "A")
                # AUR package
                log_msg "[$counter/$total] Installing AUR package: $program"
                whiptail --title "DWM Dotfiles Installation" --infobox "Installing [$counter/$total] AUR: $program\n\n$comment" 7 70
                "$AURHELPER" -S --noconfirm "$program" >> "$LOG_FILE" 2>&1
                ;;
            "G")
                # Git repository
                log_msg "[$counter/$total] Installing from Git: $program"
                whiptail --title "DWM Dotfiles Installation" --infobox "Installing [$counter/$total] Git: $program\n\n$comment" 7 70
                reponame=$(basename "$program" .git)
                mkdir -p "$HOME/.local/src"
                git clone --depth 1 "$program" "$HOME/.local/src/$reponame" >> "$LOG_FILE" 2>&1
                cd "$HOME/.local/src/$reponame" || continue
                make >> "$LOG_FILE" 2>&1
                sudo make install >> "$LOG_FILE" 2>&1
                cd "$REPO_DIR" || return 1
                ;;
            *)
                # Regular package
                log_msg "[$counter/$total] Installing package: $program"
                whiptail --title "DWM Dotfiles Installation" --infobox "Installing [$counter/$total] Package: $program\n\n$comment" 7 70
                sudo pacman --noconfirm --needed -S "$program" >> "$LOG_FILE" 2>&1
                ;;
        esac
    done < "$REPO_DIR/progs.csv"

    log_msg "✓ Package installation completed"
}

# Copy dotfiles
copy_dotfiles() {
    log_msg "Copying dotfiles to your home directory..."

    # Create directories if they don't exist
    mkdir -p "$HOME/.config"
    mkdir -p "$HOME/.local"

    # Copy .config directory
    if [ -d "$REPO_DIR/.config" ]; then
        log_msg "Copying .config directory contents..."
        cp -rf "$REPO_DIR/.config/"* "$HOME/.config/" 2>/dev/null
    fi

    # Copy .local directory (excluding .git if present)
    if [ -d "$REPO_DIR/.local" ]; then
        log_msg "Copying .local directory contents (excluding src)..."
        for item in "$REPO_DIR/.local"/*; do
            if [ -e "$item" ] && [ "$(basename "$item")" != "src" ] && [ "$(basename "$item")" != ".git" ]; then
                cp -rf "$item" "$HOME/.local/" 2>/dev/null
            fi
        done
    fi

    # Create .local/src directory if it doesn't exist
    mkdir -p "$HOME/.local/src"

    # Copy shell profiles
    for file in .zprofile .bashrc .zshrc; do
        if [ -f "$REPO_DIR/$file" ]; then
            log_msg "Copying $file to home directory..."
            cp -f "$REPO_DIR/$file" "$HOME/" 2>/dev/null
        fi
    done

    log_msg "✓ Dotfiles copied successfully"
}

# Build and install Suckless programs
build_suckless() {
    log_msg "Building and installing Suckless programs..."

    # List of Suckless programs to build
    programs=("dwm-flexipatch" "st" "dwmblocks" "slock-flexipatch")

    # Ensure target directory exists
    mkdir -p "$HOME/.local/src"

    # Build each program
    for program in "${programs[@]}"; do
        if [ -d "$REPO_DIR/.local/src/$program" ]; then
            log_msg "Building $program..."
            whiptail --infobox "Building $program..." 7 60

            # Copy program directory to user's .local/src
            log_msg "Copying $program source files..."
            cp -r "$REPO_DIR/.local/src/$program" "$HOME/.local/src/"

            # Build and install
            log_msg "Building and installing $program..."
            cd "$HOME/.local/src/$program" || {
                log_msg "Error: Could not change to directory $HOME/.local/src/$program"
                continue
            }
            make clean >> "$LOG_FILE" 2>&1
            make >> "$LOG_FILE" 2>&1
            sudo make install >> "$LOG_FILE" 2>&1
            log_msg "✓ $program installed"
        else
            log_msg "Warning: $program directory not found in $REPO_DIR/.local/src/"
        fi
    done

    cd "$REPO_DIR" || {
        log_msg "Error: Could not return to repository directory"
        return 1
    }

    log_msg "✓ Suckless programs installation completed"
}

# Display completion message
completion_message() {
    whiptail --title "Installation Complete!" \
        --msgbox "DWM Dotfiles have been installed successfully!\n\nYour original configuration has been backed up to:\n$BACKUP_DIR\n\nTo restore your previous configuration, run:\n$RESTORE_SCRIPT\n\nTo start DWM, log out and run 'startx'." 15 70
}

# Main function
main() {
    echo "----- DWM Dotfiles Installer -----"
    echo "Installation started at: $(date)"
    echo "Log file: $LOG_FILE"
    echo "----------------------------------"

    # Check if running on Arch-based system
    check_arch_system

    # Ensure whiptail is installed
    check_dependencies

    # Welcome message
    welcome_message

    # Confirm installation
    confirm_installation

    # Create backup
    create_backup

    # Create restore script
    create_restore_script

    # Install base dependencies
    log_msg "Installing base dependencies..."
    whiptail --infobox "Installing base dependencies..." 7 60
    sudo pacman --noconfirm --needed -S base-devel git curl >> "$LOG_FILE" 2>&1
    log_msg "✓ Base dependencies installed"

    # Install AUR helper
    install_aur_helper

    # Install packages from progs.csv
    install_packages

    # Copy dotfiles
    copy_dotfiles

    # Build and install Suckless programs
    build_suckless

    # Show completion message
    completion_message

    # Cleanup
    log_msg "Cleaning up..."

    echo "----------------------------------"
    log_msg "Installation completed successfully!"
    echo "To start DWM, log out and run 'startx'."
    echo "----------------------------------"
}

# Run main function
main "$@" | tee -a "$LOG_FILE"
