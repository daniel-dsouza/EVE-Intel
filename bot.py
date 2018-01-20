import discord
from discord.ext import commands

from esi import common
from esi.system import create_system


VERSION = 'v0.2'


bot = commands.Bot(command_prefix='?', description='rewrite')
common.session = bot.http.session  # is this hackish? Yes. Yes it is.


@bot.event
async def on_ready():
    latest_semver = await common.get_latest_release()
    if VERSION != latest_semver:
        print("You are running version {}. Please upgrade to {}".format(VERSION, latest_semver))
    else:
        print("You are running version {}.".format(VERSION))

    system = await create_system(name='BQ0-UU')
    print(system.objectID)

bot.run('MjkyMzYzMzQzMzkyNjY5NzA3.DTcAxw.iNSdUsDly_daT4GSc21pX_dQ6Xk')