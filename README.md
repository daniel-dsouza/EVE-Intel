# EVE-bot
I wanted a Discord bot for EVE, but I didn't want one that could leak sensitive information. So I made my own.

If you find this useful, please tell `spicy indian` in game with a mail and/or ISK donation!

## What does EVE-bot do?
This is still a work in progress, and this list will grow.

### Intel Tracking
The primary purpose for EVE-bot is to scrape the alliance intel channel for suspicious activity near our system.
You also get text-to-speech messages, provided you have the intel text channel open in Discord.

## Usage
1. Download the latest release, and unzip the file.
1. Create the eve-bot.cfg file
1. Run bot.exe
1. Launch EVE. Make sure that you log in __after__ launching the bot, or the bot will not be able to find the files!

### Commands
1. __!watch system_name__ - creates a new channel with alerts relative that system.
1. __!unwatch system_name__ - removes the channel. Do not manually delete intel channels.
1. __!shutdown__ - shuts the bot down.

### eve-bot.cfg
Here's what to put in eve-bot.cfg. You should not use quotes, unless quotes are used in the example.

To get your own discord bot token, you will need make a bot user.

```
[discord]
token = your discord bot token, no quotes
dev_token = (optional) your discord bot token, used over token

[intel]
eve_channels = [
    "EVE chat channel 1",
    "EVE chat channel 20"]
jump_range = 20 (optional)
tts_jump_range = 9 (optional)
```
