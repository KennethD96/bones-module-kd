bones-module-kd
===============

A simple module for Bones IRC-Bot featuring:
- Password Generator (SSL is recommended)
- Calculator (Requires `BC` installed on the host)
- HEX/Binary/Decimal converter
- Simple MOTD function
- Trigger manual lookup (Similar to UNIX man)
- fortune (Same as UNIX fortune. Must also be installed)
- killstreak (A trigger mimicking the death messages appearing in `Minecraft`)
- Minecraft Color-Code converter to use with the JSON tag format.
- Clock with time-zone support (ISO 3166-1 alpha-2 or the "Region/City" format) as well as UNIX-timestamp.
- Magic 8-Ball emulator
- Customizable countdown timer

For more information on the triggers consult the manual pages in the `etc/man` directory or the 'man' trigger.

Requirements:
- [Bones IRC Bot][bones] from the `feature/docs-and-cleanup` branch

Installation:
 1. Clone or copy this repo to `bones_root_path/kd/essentials/`
 2. Add the modules of your choice to the config. (See `docs/sampleconf.ini` for examples)
 3. Start your bot

[bones]: https://github.com/404d/Bones-IRCBot
