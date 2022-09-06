#!/usr/bin/env python3

# <bitbar.title>Homebrew upgrades</bitbar.title>
# <bitbar.version>v0.1.0</bitbar.version>
# <bitbar.author>junk1tm</bitbar.author>
# <bitbar.author.github>junk1tm</bitbar.author.github>
# <bitbar.desc>List and upgrade outdated Homebrew packages</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/junk1tm/swiftbar-plugins/main/screenshots/homebrew_upgrades.png</bitbar.image>
# <bitbar.dependencies>python3 brew</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/junk1tm/swiftbar-plugins#homebrew-upgrades</bitbar.abouturl>

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import json
import subprocess
from dataclasses import dataclass

import plugin

PLUGIN_ICON = "🍺"


@dataclass
class Package:
    def __init__(self, name: str, current_version: str, **_: object):
        self.name = name
        self.current_version = current_version


def main():
    cmd = subprocess.run(
        ["brew", "outdated", "--json"],
        check=True,
        text=True,
        capture_output=True,
    )

    data = json.loads(cmd.stdout)
    formulas = [Package(**obj) for obj in data["formulae"]]
    casks = [Package(**obj) for obj in data["casks"]]

    total = len(formulas) + len(casks)
    if total == 0:
        return

    plugin.print_menu_item(PLUGIN_ICON)
    plugin.print_menu_separator()

    plugin.print_menu_action(
        f"Upgrade {total} package(s)",
        ["brew", "upgrade"],
        background=True,
        refresh=True,
        sfimage="arrow.up.square",
    )

    print_group("Formulas", formulas)
    print_group("Casks", casks)


def print_group(title: str, packages: list[Package]):
    if len(packages) == 0:
        return

    plugin.print_menu_separator()
    plugin.print_menu_item(title)

    longest_name_length = max(len(pkg.name) for pkg in packages)

    for pkg in packages:
        plugin.print_menu_action(
            f"{pkg.name:<{longest_name_length}}   {pkg.current_version}",
            ["brew", "upgrade", pkg.name],
            background=True,
            refresh=True,
            sfimage="shippingbox",
            font="SFMono-Regular",  # use a monospaced font for a proper alignment
        )


if __name__ == "__main__":
    main()
