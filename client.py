import discord
import asyncio
import datetime
import configparser
import json

import system_status
import esi_routes
import log_reader

config = configparser.ConfigParser()
config.read('eve-bot.cfg')

client = discord.Client()

async def watch_intel():
    await client.wait_until_ready()
    await asyncio.sleep(1)

    channel_name = config['intel']['discord_channel'] if 'discord_channel' in config['intel'] else 'general'

    channel_list = list(client.get_all_channels())
    intel_channel = next((x for x in channel_list if x.name == channel_name), channel_list[0])
    print("Putting intel in the '{0}' channel".format(intel_channel.name))

    if 'eve_channels' in config['intel']:
        game_channels = json.loads(config.get('intel', 'eve_channels'))
        intel_channels = log_reader.LogReader(game_channels, '\Documents\EVE\logs\Chatlogs')
        log_reader.start_observer()
    else:
        print("No EVE channels listed in config. Not parsing for intel.")
        return

    while not client.is_closed:
        await asyncio.sleep(2)

        try:
            intel = intel_channels.read_logs()
            if intel is None:
                raise Exception("no intel found")

            neutrals = system_status.process_new_intel(intel)
            for n in neutrals:
                if n[1] < 2:
                    await client.send_message(intel_channel, "Safe the fuck up! Neutrals next door in {0}.".format(n[0]), tts=True)
                elif n[1] < 4:
                    await client.send_message(intel_channel, "Neutral in the pocket in {0}, {1} jumps away.".format(n[0], n[1]), tts=True)
                elif n[1] < 9:
                    await client.send_message(intel_channel, "Neutral {0} jumps away in {1}.".format(n[1], n[0]), tts=True)
                elif n[1] < 12:
                    await client.send_message(intel_channel, "Neutral {0} jumps away in {1}.".format(n[1], n[0]))

        except Exception as e:
            # print(e)
            pass


def watch(message: discord.Message):
    system = message.content[7:]
    print(system)
    print(esi_routes.get_system_id(system))




@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return  # we do not want the bot to reply to itself!

    options = {
            '.watch': watch,
            '.unwatch': 3
        }

    for option, function in options.items():
        if message.content.startswith(option):
            function(message)
            break


@client.event
async def on_ready():
    print('Logged in as {0} with userID {1}'.format(client.user.name, client.user.id))


if __name__ == '__main__':
    # client.loop.create_task(watch_intel())
    loop = asyncio.get_event_loop()

    try:
        try:
            token = config['discord']['dev_token'] if 'dev_token' in config['discord'] else config['discord']['token']
            loop.run_until_complete(client.start(token))
        except KeyError:
            print("Could not find token in config file. Please check that 'token' exists under [discord].")

    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
        log_reader.observer.stop()
    finally:
        loop.close()
        log_reader.observer.join()
