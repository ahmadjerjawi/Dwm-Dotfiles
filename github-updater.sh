#!/bin/bash

# Define directories to backup
BACKUP_DIRS=(
    "local/src"
    "local/bin"
    "local/share/chars"
    "local/share/nemo"
)

CONFIG_DIRS=(
    "mpv"
    "dunst"
    "ncmpcpp"
    "nvim"
    "pinentry"
    "pipewire"
    "pulse"
    "shell"
    "wget"
    "x11"
	"picom"
	"autin"
)

# Error handling function
handle_error() {
    echo "Error: $1"
    exit 1
}

# Create base directories if they don't exist
echo "Creating directory structure..."
mkdir -p .local/share || handle_error "Failed to create .local directory structure"
mkdir -p .config || handle_error "Failed to create .config directory"

# Backup local directories
echo "Backing up local directories..."
for dir in "${BACKUP_DIRS[@]}"; do
    if [ -d "$HOME/.${dir}" ]; then
        mkdir -p ".${dir%/*}" # Create parent directory if needed
        # Use rsync with delete flag to remove files that don't exist in source
        rsync -av --delete --exclude='.git/' "$HOME/.${dir}/" ".${dir}/" || handle_error "Failed to copy $dir"
        echo "✓ Synchronized .$dir"
    else
        echo "! Directory $HOME/.${dir} does not exist, skipping..."
        # If the directory doesn't exist in source but exists in destination, remove it
        if [ -d ".${dir}" ]; then
            echo "Removing .${dir} as it no longer exists in source..."
            rm -rf ".${dir}"
        fi
    fi
done

# Backup config directories
echo "Backing up config directories..."
for dir in "${CONFIG_DIRS[@]}"; do
    if [ -d "$HOME/.config/$dir" ]; then
        # Use rsync with delete flag to remove files that don't exist in source
        rsync -av --delete --exclude='.git/' "$HOME/.config/$dir/" ".config/$dir/" || handle_error "Failed to copy .config/$dir"
        echo "✓ Synchronized .config/$dir"
    else
        echo "! Directory $HOME/.config/$dir does not exist, skipping..."
        # If the directory doesn't exist in source but exists in destination, remove it
        if [ -d ".config/$dir" ]; then
            echo "Removing .config/$dir as it no longer exists in source..."
            rm -rf ".config/$dir"
        fi
    fi
done

# Backup shell config files
echo "Backing up shell configuration..."
for file in ".zshrc" ".zprofile"; do
    if [ -f "$HOME/$file" ]; then
        cp -L "$HOME/$file" "./$file" || handle_error "Failed to copy $file"
        echo "✓ Copied $file"
    else
        echo "! File $HOME/$file does not exist, removing if present..."
        [ -f "./$file" ] && rm "./$file"
    fi
done

# Clean up any sensitive information
echo "Cleaning up sensitive information..."
if [ -f ".config/python/pypirc" ]; then
    rm ".config/python/pypirc"
    echo "✓ Removed pypirc file"
fi

# Remove any temporary or cache files
find . -name "*.cache" -delete
find . -name ".DS_Store" -delete
find . -name "*.log" -delete

# Git operations
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Committing changes to git..."

    # Stage all changes, including deletions
    git add -A || handle_error "Failed to stage files"

    # Get current date for commit message
    current_date=$(date +"%Y-%m-%d")

    # Create commit
    git commit -m "Updated dotfiles: ${current_date}" || {
        echo "No changes to commit"
        exit 0
    }

    # Push changes if remote exists
    if git remote get-url origin >/dev/null 2>&1; then
        echo "Pushing changes to remote repository..."
        git push --force origin main || handle_error "Failed to push changes"
    else
        echo "No remote repository configured"
    fi
else
    echo "Not a git repository"
fi

echo "Backup completed successfully!"
