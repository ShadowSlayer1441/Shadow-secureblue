#!/usr/bin/env bats

setup() {
    sudo mkdir -p /usr/share/ublue-os/just/
    sudo mkdir -p /usr/share/bluebuild/justfiles/
    sudo mkdir -p /usr/lib/ujust/


    sudo cp -fr files/system/usr/lib/ujust /usr/lib/ujust
    sudo cp -f files/system/usr/bin/ujust /usr/bin/ujust
    sudo cp -f files/system/usr/share/ublue-os/just/60-custom.just /usr/share/ublue-os/just/
    sudo cp -f files/system/usr/share/ublue-os/justfile /usr/share/ublue-os/
    sudo cp -f files/justfiles/*.just /usr/share/bluebuild/justfiles/
    for filepath in /usr/share/bluebuild/justfiles/*.just; do
        sudo sh -c "echo \"import '$filepath'\" >> /usr/share/ublue-os/just/60-custom.just"
    done
}

@test "Ensure ujust is configured correctly for tests" {
    run ujust bios
    [ "$status" -eq 0 ]
}

@test "Ensure motd toggle functions properly" {
    run ujust toggle-user-motd
    [ "$status" -eq 0 ]
    [ -f "${HOME}/.config/no-show-user-motd" ]
    run ujust toggle-user-motd
    [ "$status" -eq 0 ]
    [ ! -f "${HOME}/.config/no-show-user-motd" ]
}

@test "Ensure bash lockdown works" {
    echo "$(just -V)"
    BASH_ENV_FILES=(
        "$HOME/.bashrc"
        "$HOME/.bash_profile"
        "$HOME/.config/bash-completion"
        "$HOME/.profile"
        "$HOME/.bash_logout"
        "$HOME/.bash_login"
      )
    BASH_ENV_DIRS=(
        "$HOME/.bashrc.d/"
        "$HOME/.config/environment.d/"
      )
    for file in "${BASH_ENV_FILES[@]}"; do
        before=$(lsattr "$file" 2>/dev/null)
        ujust toggle-bash-environment-lockdown true false
        after=$(lsattr "$HOME/.bashrc" 2>/dev/null)
        [[ "$before" == "$after" ]] && exit 1 
    done
    for dir in "${BASH_ENV_DIRS[@]}"; do
        before=$(lsattr  -a "$dir" 2>/dev/null | grep -c 'i----')
        ujust toggle-bash-environment-lockdown true false
        after=$(lsattr  -a "$dir" 2>/dev/null | grep -c 'i----')
        [[ "$before" == "$after" ]] && exit 1 
    done
}
