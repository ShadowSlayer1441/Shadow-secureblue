"""
override_module.py

This module overrides if a specific module is loaded via modprobe rules.
"""

# Copyright 2025 The Secureblue Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess  # nosec
import sys
import os
from pathlib import Path
from typing import Final

MOD_HELP: Final[str] = """
This python script allows the user to easily enable or disable a specific
kernel module via a new modprobe file created at "/etc/modprobe.d/". This 
script will accept any kernel module name or alias found in modules.alias
file. Note that any change this script makes will only apply after a reboot.

usage:
ujust override-module status <module name>
    Will return if the module is currently avaliable and if a modprobe 
    override appears to exist and what kind of override it is.

ujust override-module enable <module name>
    Will create a modprobe override to enable the given module assuming
    it does not already exist.

ujust override-module disable <module name>
    Will create a modprobe override to disable the given module assuming
    it does not already exist.

ujust override-module toggle <module name>
    Will toggle any existing modprobe file or create a modprobe opposite
    whether the module is currently loaded.

ujust override-module remove <module name>
    Will remove any existing modprobe override for the given module, 
    assuming the override follows the convention used by this script.

ujust override-module help
    Displays this message.
"""

def module_check(module: str) -> bool:
    """Checks if a given string is a valid module name or alias"""
    return False

def run_inner(enable: bool, module: str) -> int:
    """Runs innerscript and passes whether it should disable or enable"""

def is_module_loaded(module_name: str) -> bool:
    """Checks if a given kernel module is currently loaded by checking for it in /proc/modules"""
    try:
        with open("/proc/modules", encoding="utf8") as fd:
            return any(line.startswith(module_name + " ") for line in fd)
    except OSError:
        return False

def status(module: str) -> None:
    """Gives status of a module, both currently and what it will be after a reboot."""
    message: str = ""
    module_file: str = (f"/etc/modprobe.d/99-{module}.conf")
    override: bool = Path(module_file).exists()
    enable: bool = False
    if override:
        with open(module_file, "r", encoding="utf-8", errors="ignore") as fd:
            for line in fd:
                if "/bin/true" in line:
                    enable = False
                else:
                    enable = True
    if not is_module_loaded(module):
        message += f"{module} is disabled currently"
    else:
        message += f"{module} is enabled currently"
    if override:
        if enable:
            message += f", and after a reboot, {module} will be enabled by a modprobe override."
        else:
            message += f", and after a reboot, {module} will be disabled by a modprobe override."
    else:
        message += f", and after a reboot, the default behavior will occur (no modprobe override appears to exist)."
    print(message)

def main():

