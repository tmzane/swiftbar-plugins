# SwiftBar plugins

A collection of my plugins for [SwiftBar][swiftbar] (also compatible with
[xbar][xbar]).

## 📦 Install

1. [Install SwiftBar][install-swiftbar] (if not already)

2. Clone this repository

```shell
git clone https://github.com/junk1tm/swiftbar-plugins.git
```

3. Create a symlink to the selected plugin in your [SwiftBar plugin folder][swiftbar-plugin-folder]

```shell
ln -s /path/to/repo/plugin_name.py $SWIFTBAR_PLUGINS_PATH/plugin_name.py
```

## 🔌 Plugins

* [Docker containers](#docker-containers)
* [Homebrew upgrades](#homebrew-upgrades)
* [Pomodoro timer](#pomodoro-timer)
* [Unmount disk](#unmount-disk)

Most plugins support configuration via the top-level constants, such as
`PLUGIN_ICON`. Feel free to modify them for your needs.

### Docker containers

![screenshot](screenshots/docker_containers.png)

Switch between Docker contexts and list running containers. Click on one to open
its log in a separate terminal tab.

### Homebrew upgrades

![screenshot](screenshots/homebrew_upgrades.png)

List and upgrade outdated Homebrew packages. Works best with the
[built-in autoupdate mechanism][homebrew-autoupdate].

### Pomodoro timer

![screenshot](screenshots/pomodoro_timer.png)

The [Pomodoro timer][pomodoro] in your menu bar: start it with a single click!

### Unmount disk

Quickly unmount an external drive without need to open Finder or Disk Utility.

[swiftbar]: https://github.com/swiftbar/SwiftBar
[xbar]: https://github.com/matryer/xbar
[install-swiftbar]: https://github.com/swiftbar/SwiftBar#how-to-get-swiftbar
[swiftbar-plugin-folder]: https://github.com/swiftbar/SwiftBar#plugin-folder
[homebrew-autoupdate]: https://docs.brew.sh/Manpage#autoupdate-subcommand-interval-options
[pomodoro]: https://en.wikipedia.org/wiki/Pomodoro_Technique
