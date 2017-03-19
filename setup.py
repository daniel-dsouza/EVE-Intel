import sys
from cx_Freeze import setup, Executable

setup(
    name='eve-bot',
    version='0.0.1',
    description='It builds',


    options={
        'build_exe': {
            'packages': ['encodings', 'asyncio']
        },
    },

    executables=[Executable("bot.py")],
)
