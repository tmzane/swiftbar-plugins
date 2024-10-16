#!/usr/bin/env python3

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
# <swiftbar.environment>[HOMEBREW_NO_ANALYTICS=1, HOMEBREW_NO_AUTO_UPDATE=1]</swiftbar.environment>

import json
import subprocess
from dataclasses import dataclass

import plugin

PLUGIN_ICON = "🍺"
BREW_PATH = "/opt/homebrew/bin/brew"  # default location for Apple silicon


@dataclass
class Package:
    def __init__(self, name: str, current_version: str, **_: object):
        self.name = name
        self.current_version = current_version


def main() -> None:
    dump = subprocess.check_output([BREW_PATH, "list", "--installed-on-request"], text=True)
    manually_installed = {line for line in dump.splitlines()}

    outdated = subprocess.check_output([BREW_PATH, "outdated", "--json"], text=True)
    data = json.loads(outdated)

    formulas = [Package(**obj) for obj in data["formulae"] if obj["name"] in manually_installed]
    casks = [Package(**obj) for obj in data["casks"]]

    total = len(formulas) + len(casks)
    if total == 0:
        return

    plugin.print_menu_item(PLUGIN_ICON)
    plugin.print_menu_separator()

    plugin.print_menu_action(
        f"Upgrade {total} package(s)",
        [BREW_PATH, "upgrade"],
        refresh=True,
        sfimage="arrow.up.square",
    )

    print_group("Formulas", formulas)
    print_group("Casks", casks)


def print_group(title: str, packages: list[Package]) -> None:
    if len(packages) == 0:
        return

    plugin.print_menu_separator()
    plugin.print_menu_item(title)

    longest_name_length = max(len(pkg.name) for pkg in packages)

    for pkg in packages:
        plugin.print_menu_action(
            f"{pkg.name:<{longest_name_length}}   {pkg.current_version}",
            [BREW_PATH, "upgrade", pkg.name],
            refresh=True,
            sfimage="shippingbox",
            font="SFMono-Regular",  # use a monospaced font for a proper alignment
        )


if __name__ == "__main__":
    main()
