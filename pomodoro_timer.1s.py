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
import subprocess

import plugin

PLUGIN_ICON = "🍅"
MONOSPACED_FONT = "SFMono-Regular"
WORK_INTERVAL = datetime.timedelta(minutes=25)

OSASCRIPT_PATH = "/usr/bin/osascript"
NOTIFICATION_ON = True
NOTIFICATION_TEXT = "Well done! Feel free to take a break"
NOTIFICATION_SCRIPT = f'display notification "{NOTIFICATION_TEXT}" with title "{PLUGIN_ICON} Pomodoro Timer"'

TMP_FILE = os.path.join(os.environ["TMPDIR"], "swiftbar.pomodoro.deadline")


def main() -> None:
    # has the script been run because of a user's click?
    if os.getenv("CLICK") is not None:
        if Timer.is_ticking():
            Timer.stop()
        else:
            Timer.start()
        return

    time_prefix = ""
    if Timer.is_ticking():
        time = Timer.time_left()
        if time.total_seconds() > 0:
            minutes = time.seconds // 60
            seconds = time.seconds % 60
            time_prefix = f"{minutes:02}:{seconds:02} "
        else:
            Timer.stop()
            if NOTIFICATION_ON:
                display_notification()

    plugin.print_menu_action(
        f"{time_prefix}{PLUGIN_ICON}",
        ["CLICK=1", __file__],  # run the same script on click
        refresh=True,
        font=MONOSPACED_FONT,
    )


class Timer:
    @classmethod
    def start(cls) -> None:
        with open(TMP_FILE, "w") as f:
            deadline = datetime.datetime.now() + WORK_INTERVAL
            f.write(deadline.isoformat())

    @classmethod
    def stop(cls) -> None:
        os.remove(TMP_FILE)

    @classmethod
    def is_ticking(cls) -> bool:
        return os.path.exists(TMP_FILE)

    @classmethod
    def time_left(cls) -> datetime.timedelta:
        with open(TMP_FILE) as f:
            text = f.read()
            deadline = datetime.datetime.fromisoformat(text)
            return deadline - datetime.datetime.now()


def display_notification() -> None:
    subprocess.run([OSASCRIPT_PATH, "-e", NOTIFICATION_SCRIPT], check=True)


if __name__ == "__main__":
    main()
