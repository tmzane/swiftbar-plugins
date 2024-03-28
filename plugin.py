"""
A convenience wrapper for the SwiftBar plugin API.
See https://github.com/swiftbar/SwiftBar#plugin-api for details.
"""

import sys
import typing


class Params(typing.TypedDict, total=False):
    """
    A set of optional parameters for menu items.
    See https://github.com/swiftbar/SwiftBar#parameters for descriptions.
    """

    # text formatting:
    color: str
    sfcolor: str
    font: str
    size: int
    md: bool
    sfsize: int
    length: int
    trim: bool
    ansi: bool
    emojize: bool
    symbolize: bool

    # visuals:
    dropdown: bool
    alternate: bool
    image: str
    templateImage: str
    sfimage: str
    checked: bool
    tooltip: str

    # actions:
    refresh: bool
    href: str
    shortcut: str
    # the following parameters are set automatically when using print_action():
    shell: str
    # param1: str
    # param2: str
    # ...
    # paramN: str
    terminal: bool


class Writer(typing.Protocol):
    """
    Anything that supports write.
    """

    def write(self, _: str, /) -> int: ...


def print_menu_item(text: str, *, out: Writer = sys.stdout, **params: typing.Unpack[Params]) -> None:
    """
    Print a read-only menu item.
    """

    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    print(f"{text} | {params_str}", file=out)


def print_menu_action(
    text: str,
    cmd: list[str],
    *,
    open_terminal: bool = False,
    out: Writer = sys.stdout,
    **params: typing.Unpack[Params],
) -> None:
    """
    Print an interactive menu item that runs the provided command on click.
    """

    if len(cmd) > 0:
        params["shell"] = cmd[0]
        for i, arg in enumerate(cmd[1:]):
            params[f"param{i}"] = arg  # type: ignore

        params["terminal"] = open_terminal

    print_menu_item(text, out=out, **params)


def print_menu_separator(*, out: Writer = sys.stdout) -> None:
    """
    Print a menu separator.
    """

    print("---", file=out)
