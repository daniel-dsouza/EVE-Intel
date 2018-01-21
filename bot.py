__version__ = 'v0.4'


import configparser
from discord.ext import commands
import os

from esi import common
from esi.eve_types import System


bot = commands.Bot(command_prefix='?', description='rewrite')
common.session = bot.http.session  # is this hackish? Yes. Yes it is.
config = configparser.ConfigParser()


@bot.event
async def on_ready():
    latest_semver = await common.get_latest_release()
    if __version__ != latest_semver:
        print("You are running version {}. Please upgrade to {}".format(__version__, latest_semver))
    else:
        print("You are running version {}.".format(__version__))

    system = await System.new(name='BQ0-UU')
    print(system.objectID)

if __name__ == '__main__':
    try:
        if not os.path.exists('eve-intel.cfg'):
            raise FileNotFoundError

        config.read('eve-intel.cfg')
        token = config.get('discord', 'token')
        bot.run(token)
    except FileNotFoundError as e:
        print('Could not find configuration file "eve-intel.cfg" in this directory.')
    except configparser.NoSectionError or configparser.NoOptionError as e:
        print(e)
    finally:
        bot.close()
