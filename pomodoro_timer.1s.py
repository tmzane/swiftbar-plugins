#!/usr/bin/env python3

# <bitbar.title>Pomodoro timer</bitbar.title>
# <bitbar.version>v0.1.0</bitbar.version>
# <bitbar.author>junk1tm</bitbar.author>
# <bitbar.author.github>junk1tm</bitbar.author.github>
# <bitbar.desc>The Pomodoro timer in your menu bar: start it with a single click</bitbar.desc>
# <bitbar.image>https://raw.githubusercontent.com/junk1tm/swiftbar-plugins/main/screenshots/pomodoro_timer.png</bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://github.com/junk1tm/swiftbar-plugins#pomodoro-timer</bitbar.abouturl>

# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>

import datetime
import os

import plugin

PLUGIN_ICON = "🍅"
WORK_INTERVAL = datetime.timedelta(minutes=25)
TMP_FILE = os.path.join(os.environ["TMPDIR"], "swiftbar.pomodoro.deadline")


def main():
    # a special environment variable indicating that
    # the script has been run because a user has clicked the icon
    CLICKED_ENV_VAR = "CLICKED"

    if os.getenv(CLICKED_ENV_VAR) is not None:
        on_click()
        return

    time_prefix = ""
    if os.path.exists(TMP_FILE):
        with open(TMP_FILE, "r") as f:
            deadline = datetime.datetime.fromisoformat(f.read())
            diff = deadline - datetime.datetime.now()
            if diff.total_seconds() > 0:
                minutes = diff.seconds // 60
                seconds = diff.seconds % 60
                time_prefix = f"{minutes:02}:{seconds:02} "
            else:
                os.remove(TMP_FILE)

    plugin.print_menu_action(
        f"{time_prefix}{PLUGIN_ICON}",
        [f"{CLICKED_ENV_VAR}=1", "python3", __file__],
        background=True,
        refresh=True,
    )


def on_click():
    # there are two possible states when the icon is clicked:

    # 1. the timer is ticking, so we need to stop it
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)
        return

    # 2. the timer is off, so we need to start it
    with open(TMP_FILE, "w") as f:
        deadline = datetime.datetime.now() + WORK_INTERVAL
        f.write(deadline.isoformat())


if __name__ == "__main__":
    main()
