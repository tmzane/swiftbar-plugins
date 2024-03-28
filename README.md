# SwiftBar plugins

[![checks](https://github.com/tmzane/swiftbar-plugins/actions/workflows/checks.yml/badge.svg)](https://github.com/tmzane/swiftbar-plugins/actions/workflows/checks.yml)

A collection of my plugins for [SwiftBar][1] (also compatible with [xbar][2]).

## 📦 Install

Python 3.11+

1. [Install SwiftBar][3] (if not already)

2. Clone this repository

```shell
git clone https://github.com/tmzane/swiftbar-plugins
```

3. Create a symlink to the selected plugin in your [plugin folder][4]

```shell
ln -s /path/to/repo/plugin_name.py $SWIFTBAR_PLUGINS_PATH/plugin_name.py
```

## 🔌 Plugins

* [Docker containers](#docker-containers)
* [Homebrew upgrades](#homebrew-upgrades)
* [Pomodoro timer](#pomodoro-timer)

Most plugins support configuration via top-level constants, such as `PLUGIN_ICON`.
Feel free to modify them for your needs.

### Docker containers

![screenshot](screenshots/docker_containers.png)

Switch between Docker contexts and list running containers.
Click to open logs in a separate terminal tab.

### Homebrew upgrades

![screenshot](screenshots/homebrew_upgrades.png)

List outdated Homebrew packages.
Click to upgrade the selected package.

### Pomodoro timer

![screenshot](screenshots/pomodoro_timer.png)

A [pomodoro timer][5] in your menu bar.
Click to start the countdown.

[1]: https://github.com/swiftbar/SwiftBar
[2]: https://github.com/matryer/xbar
[3]: https://github.com/swiftbar/SwiftBar#how-to-get-swiftbar
[4]: https://github.com/swiftbar/SwiftBar#plugin-folder
[5]: https://en.wikipedia.org/wiki/Pomodoro_Technique
