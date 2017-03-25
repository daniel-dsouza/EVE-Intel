import asyncio
import configparser
import discord
from discord.ext import commands
import json
import os.path

import esi_routes
import log_reader
from system_status import System, IntelParser

evebot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='An intel scraper for EVE')
config = configparser.ConfigParser()


class EVEbot:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.intel_channels = {}

        game_channels = json.loads(config.get('intel', 'eve_channels'))
        self.intel_parser = IntelParser(game_channels)

        self.bot.loop.create_task(self.get_default_systems())
        self.bot.loop.create_task(self.scrape_to_systems())

    async def get_default_systems(self):
        await self.bot.wait_until_ready()
        channels = [ch for ch in self.bot.get_all_channels() if ch.name.startswith('intel-')]
        for chan in channels:
            system_name = chan.name[6:].swapcase()
            system_id = esi_routes.get_system_id(system_name)
            self.intel_channels[system_id] = (chan, System(system_name))
            print('Providing intel to {0}'.format(system_name))

    async def scrape_to_systems(self):
        await self.bot.wait_until_ready()
        self.intel_parser.start()

        await asyncio.sleep(1)  # this helps, i promise

        while not self.bot.is_closed:
            await asyncio.sleep(5)  # check for intel every 5 seconds

            intel = self.intel_parser.process_new_intel()
            if intel is None:
                continue

            for system_id, (channel, system) in self.intel_channels.items():
                i = system.add_intel(intel)
                for a, jumps in i:
                    if a.clear is True:
                        continue

                    if jumps == 0:
                        message = "Stop drop and dock! Neutral in {1.system_name}."
                    elif jumps == 1:
                        message = "Safe the fuck up! Neutral next door in {1.system_name}."
                    else:
                        message = "Neutral {0} jumps out in {1.system_name}."

                    print(message.format(jumps, a))
                    await self.bot.send_message(channel, message.format(jumps, a), tts=True if jumps < 9 else False)

    @commands.command(pass_context=True, no_pm=True)
    async def watch(self, ctx, *, system: str):
        system_id = esi_routes.get_system_id(system)
        if system_id is None:
            await self.bot.say("no such system {0}".format(system))
            return
        elif system_id in self.intel_channels:
            await self.bot.say("already watching {0}".format(system))
            return

        channel = await self.bot.create_channel(ctx.message.server, 'intel-'+system)
        self.intel_channels[system_id] = (channel, System(system))

    @commands.command(pass_context=True, no_pm=True)
    async def unwatch(self, ctx, *, system: str):
        system_id = esi_routes.get_system_id(system)
        if system_id is None:
            await self.bot.say("no such system {0}".format(system))
            return
        elif self.intel_channels[system_id] is None:
            await self.bot.say("no channel to remove for {0}".format(system))
            return

        await self.bot.say("removing channel {0}".format(system))
        await self.bot.delete_channel(self.intel_channels[system_id][0])
        self.intel_channels.pop(system_id)


@evebot.event
async def on_ready():
    print('Logged in as: {0} (ID: {0.id})'.format(evebot.user))

if __name__ == '__main__':
    try:
        config.read('eve-bot.cfg')
        if not os.path.exists('eve-bot.cfg'):
            raise FileNotFoundError
    except FileNotFoundError as e:
        print('Could not find any filed named "eve-bot.cfg" in this directory.')
        input('Press ENTER to quit')
        exit()

    evebot.add_cog(EVEbot(evebot))

    try:
        token = config['discord']['dev_token'] if 'dev_token' in config['discord'] else config['discord']['token']
        evebot.run(token)
    except KeyError:
        print("Could not find token in config file. Please check that 'token' exists under [discord].")
