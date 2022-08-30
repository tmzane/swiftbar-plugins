#!/usr/bin/env python3

# <bitbar.title>Docker containers</bitbar.title>
# <bitbar.version>v0.1.0</bitbar.version>
# <bitbar.author>junk1tm</bitbar.author>
# <bitbar.author.github>junk1tm</bitbar.author.github>
# <bitbar.desc>Switch between Docker contexts and list running containers</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/junk1tm/swiftbar-plugins/main/screenshots/docker_containers.png</bitbar.image>
# <bitbar.dependencies>python3 docker</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/junk1tm/swiftbar-plugins#docker-containers</bitbar.abouturl>

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import json
import subprocess
from dataclasses import dataclass

import plugin

PLUGIN_ICON = "🐋"


@dataclass(frozen=True)
class Context:
    name: str
    current: bool


@dataclass(frozen=True)
class Container:
    name: str
    status: str


def main():
    plugin.print_menu_item(PLUGIN_ICON)
    plugin.print_menu_separator()
    plugin.print_menu_item("Context")

    cmd = subprocess.run(
        ["docker", "context", "list", "--format=json"],
        check=True,
        text=True,
        capture_output=True,
    )

    objects = list(json.loads(cmd.stdout))
    contexts = [Context(obj["Name"], obj["Current"]) for obj in objects]

    for ctx in contexts:
        plugin.print_menu_action(
            ctx.name,
            ["docker", "context", "use", ctx.name],
            background=True,
            refresh=True,
            checked=ctx.current,
        )

    plugin.print_menu_separator()
    plugin.print_menu_item("Containers")

    try:
        cmd = subprocess.run(
            ["docker", "ps", "--format={{.Names}}\t{{.Status}}"],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        plugin.print_menu_item("docker daemon is not running", color="red")
        return

    containers = [Container(*line.split("\t")) for line in cmd.stdout.splitlines()]
    longest_name_length = max(len(ctn.name) for ctn in containers)

    for ctn in containers:
        plugin.print_menu_action(
            f"{ctn.name:<{longest_name_length}}   {ctn.status}",
            ["docker", "logs", ctn.name],
            font="SFMono-Regular",  # use a monospaced font for a proper alignment
        )


if __name__ == "__main__":
    main()
