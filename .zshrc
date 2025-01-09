# Source custom Zsh scripts
for script in ~/.config/atuin/*.zsh; do
    source "$script"
done
export THEOS=$HOME/theos
export SERVER_ROOT=%(pwd)
# Disable default key bindings
export ATUIN_NOBIND="true"
eval "$(atuin init zsh --disable-up-arrow)"

# Bind Atuin to up arrow + Shift
bindkey '^[[1;2A' atuin-up-search
