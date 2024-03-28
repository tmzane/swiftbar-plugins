#!/usr/bin/env python3

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import json
import subprocess
from dataclasses import dataclass

import plugin

PLUGIN_ICON = "🐋"
DOCKER_PATH = "/usr/local/bin/docker"
MONOSPACED_FONT = "SFMono-Regular"


@dataclass(frozen=True)
class Context:
    name: str
    current: bool


@dataclass(frozen=True)
class Container:
    name: str
    status: str


def main() -> None:
    plugin.print_menu_item(PLUGIN_ICON)
    plugin.print_menu_separator()
    plugin.print_menu_item("Context")

    cmd = subprocess.run(
        [DOCKER_PATH, "context", "list", "--format=json"],
        check=True,
        text=True,
        capture_output=True,
    )

    objects = list(json.loads(cmd.stdout))
    contexts = [Context(obj["Name"], obj["Current"]) for obj in objects]

    for ctx in contexts:
        plugin.print_menu_action(
            ctx.name,
            [DOCKER_PATH, "context", "use", ctx.name],
            refresh=True,
            checked=ctx.current,
        )

    plugin.print_menu_separator()
    plugin.print_menu_item("Containers")

    try:
        cmd = subprocess.run(
            [DOCKER_PATH, "ps", "--format={{.Names}}\t{{.Status}}"],
            check=True,
            text=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        plugin.print_menu_item("docker daemon is not running", color="red")
        return

    containers = [Container(*line.split("\t")) for line in cmd.stdout.splitlines()]
    if len(containers) == 0:
        return

    longest_name_length = max(len(ctn.name) for ctn in containers)

    for ctn in containers:
        plugin.print_menu_action(
            f"{ctn.name:<{longest_name_length}}   {ctn.status}",
            [DOCKER_PATH, "logs", ctn.name],
            open_terminal=True,
            font=MONOSPACED_FONT,  # use a monospaced font for a proper alignment
        )


if __name__ == "__main__":
    main()
