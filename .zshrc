# shellcheck disable=SC2034,SC2153,SC2086,SC2155

# Source custom Zsh scripts
for script in ~/.config/atuin/*.zsh; do
    source "$script"
done

# Set environment variables
export THEOS=$HOME/theos
export SERVER_ROOT=%(pwd)

eval "$( atuin init zsh --disable-up-arrow)"

# Added by LM Studio CLI (lms)
export PATH="$PATH:/home/ahmad/.lmstudio/bin"
