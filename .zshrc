# shellcheck disable=SC2034,SC2153,SC2086,SC2155

# Set environment variables
export THEOS=$HOME/theos
export SERVER_ROOT=%(pwd)

# Right to left languages support
if ! [[ "$(ps -p $(ps -p $(echo $$) -o ppid=) -o comm=)" =~ 'bicon'* ]]; then
 bicon.bin
fi
eval "$( atuin init zsh --disable-up-arrow)"
