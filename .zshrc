# shellcheck disable=SC2034,SC2153,SC2086,SC2155

# Source custom Zsh scripts
for script in ~/.config/atuin/*.zsh; do
    source "$script"
done

# Set environment variables
export THEOS=$HOME/theos
export SERVER_ROOT=%(pwd)
export ATUIN_NOBIND="true"
export ATUIN_SESSION=$(atuin uuid)

# Initialize Atuin
eval "$(atuin init zsh --disable-up-arrow)"

# Bind Atuin to up arrow + Shift
bindkey '^[[1;2A' atuin-up-search
export XDG_RUNTIME_DIR=/run/user/$(id -u)


# If zsh-autosuggestions is installed, configure it to use Atuin's search
_zsh_autosuggest_strategy_atuin() {
    suggestion=$(ATUIN_QUERY="$1" atuin search --cmd-only --limit 1 --search-mode prefix)
}

if [ -n "${ZSH_AUTOSUGGEST_STRATEGY:-}" ]; then
    ZSH_AUTOSUGGEST_STRATEGY=("atuin" "${ZSH_AUTOSUGGEST_STRATEGY[@]}")
else
    ZSH_AUTOSUGGEST_STRATEGY=("atuin")
fi

# Hook into preexec and precmd
_atuin_preexec() {
    local id
    id=$(atuin history start -- "$1")
    export ATUIN_HISTORY_ID="$id"
    __atuin_preexec_time=${EPOCHREALTIME-}
}

_atuin_precmd() {
    local EXIT="$?" __atuin_precmd_time=${EPOCHREALTIME-}
    [[ -z "${ATUIN_HISTORY_ID:-}" ]] && return
    local duration=""
    if [[ -n $__atuin_preexec_time && -n $__atuin_precmd_time ]]; then
        printf -v duration %.0f $(((__atuin_precmd_time - __atuin_preexec_time) * 1000000000))
    fi
    (ATUIN_LOG=error atuin history end --exit $EXIT ${duration:+--duration=$duration} -- $ATUIN_HISTORY_ID &) >/dev/null 2>&1
    export ATUIN_HISTORY_ID=""
}

# Search widgets
_atuin_search() {
    emulate -L zsh
    zle -I
    local output
    output=$(ATUIN_SHELL_ZSH=t ATUIN_LOG=error ATUIN_QUERY=$BUFFER atuin search $* -i 3>&1 1>&2 2>&3)
    zle reset-prompt
    if [[ -n $output ]]; then
        RBUFFER=""
        LBUFFER=$output
        if [[ $LBUFFER == __atuin_accept__:* ]]
        then
            LBUFFER=${LBUFFER#__atuin_accept__:}
            zle accept-line
        fi
    fi
}

# Add hooks
add-zsh-hook preexec _atuin_preexec
add-zsh-hook precmd _atuin_precmd

# Key bindings for Atuin search
zle -N atuin-search _atuin_search
zle -N atuin-up-search _atuin_up_search
