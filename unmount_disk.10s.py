#!/usr/bin/env python3

# <bitbar.title>Unmount disk</bitbar.title>
# <bitbar.version>v0.1.0</bitbar.version>
# <bitbar.author>junk1tm</bitbar.author>
# <bitbar.author.github>junk1tm</bitbar.author.github>
# <bitbar.desc>Quickly unmount an external drive without need to open Finder or Disk Utility</bitbar.desc>
# <bitbar.image></bitbar.image>
# <bitbar.dependencies>python3 diskutil</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/junk1tm/swiftbar-plugins#unmount-disk</bitbar.abouturl>

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import os

import plugin

PLUGIN_ICON = ":opticaldiscdrive:"
DISKUTIL_PATH = "/usr/sbin/diskutil"
MOUNT_POINT = "/Volumes/Expansion"


def main():
    if not os.path.ismount(MOUNT_POINT):
        return

    plugin.print_menu_action(
        PLUGIN_ICON,
        [DISKUTIL_PATH, "unmountDisk", MOUNT_POINT],
        background=True,
        refresh=True,
    )


if __name__ == "__main__":
    main()
