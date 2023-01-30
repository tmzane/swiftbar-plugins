"""
A convenience wrapper for the SwiftBar plugin API.
See https://github.com/swiftbar/SwiftBar#plugin-api for details.
"""

import sys
import typing

import typing_extensions as typingx


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
    # shell: str
    # params: list[str]
    # terminal: bool


class Writer(typing.Protocol):
    """
    Anything that supports write.
    """

    def write(self, _: str, /) -> int:
        ...


def print_menu_item(text: str, *, out: Writer = sys.stdout, **params: typingx.Unpack[Params]):
    """
    Print a read-only menu item.
    """

    params_str = " ".join(f"{k}={v}" for k, v in params.items())
    print(f"{text} | {params_str}", file=out)


def print_menu_action(text: str, cmd: list[str], *, background: bool = False, out: Writer = sys.stdout,
                      **params: typingx.Unpack[Params]):
    """
    Print an interactive menu item that runs the provided command on click.
    """

    untyped_params = dict(params)

    if len(cmd) > 0:
        untyped_params["shell"] = cmd[0]
        for i, arg in enumerate(cmd[1:]):
            untyped_params[f"param{i}"] = arg

        if background:
            untyped_params["terminal"] = False

    print_menu_item(text, out=out, **untyped_params)


def print_menu_separator(*, out: Writer = sys.stdout):
    """
    Print a menu separator.
    """

    print("---", file=out)
