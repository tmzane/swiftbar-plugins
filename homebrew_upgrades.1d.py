#!/usr/bin/env python3

# <bitbar.title>Homebrew upgrades</bitbar.title>
# <bitbar.version>v0.1.0</bitbar.version>
# <bitbar.author>junk1tm</bitbar.author>
# <bitbar.author.github>junk1tm</bitbar.author.github>
# <bitbar.desc>List and upgrade outdated Homebrew packages</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/junk1tm/swiftbar-plugins/main/screenshots/homebrew_upgrades.png</bitbar.image>
# <bitbar.dependencies>python3 brew</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/junk1tm/swiftbar-plugins#homebrew-upgrades</bitbar.abouturl>

# TODO(junk1tm): it's too slow to run `brew outdated` on each open, maybe use a cache?
# <swiftbar.refreshOnOpen>true</swiftbar.refreshOnOpen>

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>


import json
import os
import subprocess
import tempfile
from dataclasses import dataclass

import plugin

PLUGIN_ICON = "🍺"
BREW_PATH = "/opt/homebrew/bin/brew"  # default location for Apple silicon
MONOSPACED_FONT = "SFMono-Regular"  # a monospaced font is required for proper alignment


@dataclass
class Package:
    def __init__(self, name: str, current_version: str, **_: object):
        self.name = name
        self.current_version = current_version

    def is_upgrading(self) -> bool:
        return os.path.exists(tmpfile("*")) or os.path.exists(tmpfile(self.name))


def main() -> None:
    # TODO(junk1tm): maybe use a flag instead?
    if (pkgname := os.getenv("UPGRADE")) is not None:
        run_upgrade(pkgname)
        return

    cmd = subprocess.run(
        [BREW_PATH, "outdated", "--json"],
        check=True,
        text=True,
        capture_output=True,
    )

    data = json.loads(cmd.stdout)
    formulas = [Package(**obj) for obj in data["formulae"]]
    casks = [Package(**obj) for obj in data["casks"]]

    packages = formulas + casks
    if len(packages) == 0:
        return

    plugin.print_menu_item(PLUGIN_ICON)
    plugin.print_menu_separator()

    if (l := len([pkg for pkg in packages if pkg.is_upgrading()])) > 0:
        plugin.print_menu_item(f"Upgrading {l} package(s)", sfimage="arrow.up.square.fill")
    else:
        plugin.print_menu_action(
            f"Upgrade {len(packages)} package(s)",
            ["UPGRADE=*", __file__],
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
        text = f"{pkg.name:<{longest_name_length}}   {pkg.current_version}"
        if pkg.is_upgrading():
            plugin.print_menu_item(text, sfimage="shippingbox.fill", font=MONOSPACED_FONT)
            continue

        cmd = ["UPGRADE=" + pkg.name, __file__]
        plugin.print_menu_action(text, cmd, refresh=True, sfimage="shippingbox", font=MONOSPACED_FONT)


def run_upgrade(pkgname: str) -> None:
    # 1. create a tempfile
    pkgfile = tmpfile(pkgname)
    with open(pkgfile, "w"):
        pass

    try:
        # 2. upgrade the package
        if pkgname == "*":  # upgrade all
            subprocess.run([BREW_PATH, "upgrade"], check=True)
        else:
            subprocess.run([BREW_PATH, "upgrade", pkgname], check=True)
    except subprocess.CalledProcessError:
        # TODO(junk1tm): show an error
        pass
    finally:
        # 3. delete the tempfile
        os.remove(pkgfile)


def tmpfile(pkgname: str) -> str:
    tmpdir = tempfile.gettempdir()
    return os.path.join(tmpdir, f"swiftbar.homebrew_upgrades.{pkgname}")


if __name__ == "__main__":
    main()
