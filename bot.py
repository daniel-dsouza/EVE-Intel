import asyncio
import configparser
from discord.ext import commands
import discord
import json
import os.path
import time

from chat_reader import ChatReader
from evethings.system import System
from system_status import IntelParser
import esi_routes as esi
import message_parser


VERSION = 'v0.3'
evebot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='An intel scraper for EVE')
config = configparser.ConfigParser()


class EVEbot:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.intel_channels = {}

        self.reader = ChatReader(json.loads(config.get('intel', 'eve_channels')), '\Documents\EVE\logs\Chatlogs')

        # self.bot.loop.set_debug(True)
        self.bot.loop.create_task(self.get_default_systems())
        self.scraper_task = self.bot.loop.create_task(self.scrape_to_systems())
        self.update_task = self.bot.loop.create_task(self.update_status())

    async def get_default_systems(self):
        await self.bot.wait_until_ready()
        channels = [ch for ch in self.bot.get_all_channels() if ch.name.startswith('intel-')]
        for chan in channels:
            system = System(chan.name[6:].swapcase())
            self.intel_channels[system.objectID] = (chan, system)

        print('Providing intel to', ", ".join([x[1].name for x in self.intel_channels.values()]))

    async def scrape_to_systems(self):
        await self.bot.wait_until_ready()
        await self.reader.wait_until_ready()

        await self.bot.change_presence(game=discord.Game(name=self.reader.eve_client))

        tts_jump_range = config.getint('intel', 'tts_jump_range', fallback=9)
        jump_range = config.getint('intel', 'jump_range', fallback=20)

        while self.bot.is_logged_in:
            intel = IntelParser(jump_range=jump_range)
            messages = await self.reader.get_messages()
            for m in messages:
                intel.process_message(m)

            for system_id, (channel, home_system) in self.intel_channels.items():
                for message, jumps in intel.summarize(home_system):
                    try:
                        tts = True if jumps < tts_jump_range else False
                        await self.bot.send_message(channel, content=message, tts=tts)
                        await asyncio.sleep(1.0)  # sending messages too fast makes Discord upset
                    except Exception as ex:
                        print('Could not speak message: ', ex)

        if not self.bot.is_logged_in:
            print('bot is logged off')
        else:
            print('bot has quit for unknown reason!')

    async def update_status(self):
        await self.bot.wait_until_ready()

        while self.bot.is_logged_in:
            await asyncio.sleep(10.0)
            delta_t = time.time() - self.reader.last_updated
            game = discord.Game(name=self.reader.eve_client) if self.reader.eve_client != '' else None
            if delta_t > 600.0:
                await self.bot.change_presence(status=discord.Status.dnd, game=game)
            elif delta_t > 300.0:
                await self.bot.change_presence(status=discord.Status.idle, game=game)
            else:
                await self.bot.change_presence(status=discord.Status.online, game=game)

    @commands.command(pass_context=True, no_pm=True, help='get alerts relative to a system. !watch BQ0-UU')
    async def watch(self, ctx, *, system_name: str):
        try:
            system = System(system_name=system_name)
            if system.objectID in self.intel_channels:
                await self.bot.say("already watching {0}".format(system.name))
                return

            channel = await self.bot.create_channel(ctx.message.server, 'intel-' + system.name)
            await self.bot.say("adding channel {0}".format('intel-' + system.name))
            self.intel_channels[system.objectID] = (channel, system)
        except Exception:
            await self.bot.say("no such system {0}".format(system_name))

    @commands.command(pass_context=True, no_pm=True, help='remove the alerts channel for the system. !unwatch BQ0-UU')
    async def unwatch(self, ctx, *, system_name: str):
        try:
            system = System(system_name=system_name)
            if self.intel_channels[system.objectID] is None:
                await self.bot.say("no channel to remove for {0}".format(system.name))
                return

            await self.bot.say("removing channel {0}".format('intel-' + system.name))
            await self.bot.delete_channel(self.intel_channels[system.objectID][0])
            self.intel_channels.pop(system.objectID)
        except Exception:
            await self.bot.say("no such system {0}".format(system_name))

    @commands.command(pass_context=True, no_pm=True, help='says which EVE character the bot is pulling intel from')
    async def client(self, ctx):
        try:
            await self.bot.say('Using log files from {0}'.format(self.reader.eve_client))
        except AttributeError as error:
            await self.bot.say('I am not reading log files at the moment')

    @commands.command(pass_context=True, no_pm=True, help='remotely disconnects the bot, manual restart required')
    async def shutdown(self, ctx):
        print('Remote shutdown triggered by {0}'.format(ctx.message.author.nick))
        await self.bot.say('Remote shutdown triggered by {0}'.format(ctx.message.author.nick))
        await self.bot.logout()
        self.scraper_task.cancel()
        self.update_task.cancel()
        await self.bot.close()


@evebot.event
async def on_ready():
    print('Logged in as: {0} (ID: {0.id})'.format(evebot.user))


def shutdown():
    for task in [x for x in asyncio.Task.all_tasks() if x is 'PENDING']:
        task.cancel()

    input('\nPress ENTER to exit')
    exit()

if __name__ == '__main__':
    latest_version = esi.get_latest_stable_release()
    if latest_version != VERSION:
        print('You are running {0}. Please download {1} from Github.'.format(VERSION, latest_version))
    else:
        print('You are running the latest version.')

    try:
        config.read('eve-bot.cfg')
        if not os.path.exists('eve-bot.cfg'):
            raise FileNotFoundError
    except FileNotFoundError as e:
        print('Could not find any filed named "eve-bot.cfg" in this directory.')
        shutdown()

    message_parser.ignore_words = set([''] + json.loads(config.get('intel', 'ignored_words')))

    evebot.add_cog(EVEbot(evebot))

    try:
        token = config['discord']['dev_token'] if 'dev_token' in config['discord'] else config['discord']['token']
        evebot.run(token)
    except KeyError:
        print("Could not find token in config file. Please check that 'token' exists under [discord].")
    finally:
        shutdown()


