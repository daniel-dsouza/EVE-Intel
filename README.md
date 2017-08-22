# EVE-bot
[![Build Status](https://travis-ci.org/daniel-dsouza/eve-bot.svg?branch=master)](https://travis-ci.org/daniel-dsouza/eve-bot)

I wanted a Discord bot for EVE, but I didn't want one that could leak sensitive information. So I made my own.

If you find this useful, please tell `east indian` in game with a mail and/or an ISK donation!

## What does EVE-bot do?
This is still a work in progress, and this list will grow.

### Intel Tracking
The primary purpose for EVE-bot is to scrape the alliance intel channel for suspicious activity near our system.
You also get text-to-speech messages, provided you have the intel text channel open in Discord.

## Usage
1. __!watch system_name__ - creates a new channel with alerts relative that system.
1. __!client__ - prints the name of the EVE client currently running the bot
1. __!unwatch system_name__ - removes the channel. Do not manually delete intel channels.
1. __!shutdown__ - remotely shuts the bot down.

### Server Setup
1. Enable [developer settings](https://discordapp.com/developers/applications/me) for your Discord account.
1. Create a new app, and give it a name. EVEBot works.
1. In your following screen, Create a Bot User.
1. Record your Client ID (in App Details) and token (in the App Bot User section).
1. Fill in your Client ID, to add the bot to your server. `https://discordapp.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=80912`

### Bot Setup
1. Download the [latest stable release](https://github.com/daniel-dsouza/eve-bot/releases/latest), and unzip the file.
1. Create the eve-bot.cfg file
1. Run bot.exe
1. Launch EVE. Make sure that you log in __after__ launching the bot, or the bot will not be able to find the files!

### eve-bot.cfg
Here's what to put in `eve-bot.cfg`. You should not use quotes, unless quotes are used in the example.

To get your own discord bot token, you will need make a bot user.

```
[discord]
token = your discord bot token, no quotes
dev_token = (optional) your discord bot token, used over token
channel_overrides = (optional) [
    ["Discord Channel", "system"],
    ["another Discord channel", "another system"]]

[intel]
eve_channels = [
    "EVE chat channel 1",
    "EVE chat channel 20"]
jump_range = 20
tts_jump_range = 9
ignored_words = [
    "please", "pls",
    "help",
    "coming", "gone",
    "fleet",
    "status", "status?"]
```

## Licensing
EVE Online is a trademark of [CCP hf](https://www.ccpgames.com/).