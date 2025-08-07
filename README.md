# EXPKG - The Ultimate Package Downloader/Updater

## What's this ?

This is a very simple project, mostly aimed to satisfy my own needs of having to automate
the whole process of downloading/updating external packages from sources which are not directly
proper repos, such as GitHub for example.

Thus, EXPKG is a *simple* Python tool/script which is able to manage your external package files in a clean
way by using the famous `nvchecker` tool to track new releases. It is basically a useful wrapper around nvchecker.

I hope you'll enjoy it!

## Installation

First, install the `uv` package on your system. It basically helps managing Python dependencies in isolated environments
and it is needed as a dependency of this script, to make your life easier.

Download `expkg.py`, do a simple `chmod +x expkg.py` in your Terminal where the file is stored and launch `./expkg.py`!

But don't forget to configure EXPKG otherwise it would be quite useless!

## Documentation

As said above, EXPKG is basically a "wrapper" around `nvchecker`. As such, you will find the config file incredibly similar.
Actually, they are the same! There are just more options to make EXPKG work correctly.

**The default location for the config file is `~/.config/expkg/expkg.toml` . Use the `-c` command argument to indicate another location.** 

Here's a simple example:

```toml
[__config__]
oldver = "old_ver.json"
newver = "new_ver.json"
install_cmd = "sudo dnf install -y"

[Vesktop]
source = "github"
use_latest_release = true
github = "Vencord/Vesktop"
expkgurl = "https://github.com/Vencord/Vesktop/releases/download/${version}/vesktop-${version[1:]}.x86_64.rpm"

[YoutubeMusic]
source = "github"
use_latest_release = true
github = "th-ch/youtube-music"
expkgurl = "https://github.com/th-ch/youtube-music/releases/download/${version}/youtube-music-${version[1:]}.x86_64.rpm"
```

As you can see, everything is quite straightforward.

In the `__config__` section, you have to indicate where the version tracking files should be stored.
I recommend you not to change these locations, as they are basically not important for you.

The most important key you have to set is the `install_cmd` one, which is the command you use to automatically
install a package file. If this command is not correctly set, be ready to see EXPKG failing.

Finally, you have to describe what packages you want to download/update, all of the options are the `nvchecker` ones
so please check their documentation to see what's available to you.
The only EXPKG option you have to set for each package is the `expkgurl` option.

It is basically the URL pointing to the file you want to download on each release. As such, it shouldn't depend on the
current version of the software. To be able to do that, EXPKG parses every `${...}` block as Python code, which is
useful to make simple operations to manipulate the different available variables (`package` and `version`) in the URL.

