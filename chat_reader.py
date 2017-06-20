import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from os.path import expanduser, basename
import codecs

import asyncio


def prefix(path):
    return basename(path)[:basename(path).find('_2')]  # will not work after the year 2999


class MyHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        PatternMatchingEventHandler.__init__(self, patterns=patterns)
        self.files = {}
        self.eve_client = ''

    def on_created(self, event):
        time.sleep(0.1)  # delay needed to open files.
        with codecs.open(event.src_path, 'r', 'utf-16') as log:
            if prefix(log.name) not in [prefix(x) for x in self.files]: # do not log from multiple clients
                a = log.readlines()
                c = list(filter(lambda x: x != "", a[8].rstrip().split(" ")))  # read the eve_client
                self.eve_client = " ".join(c[1:])
                print("using {0} to read '{1}'".format(log.name, prefix(log.name)))
                self.files[event.src_path] = log.tell()

    def read(self):
        data = []
        for path, index in self.files.items():
            with codecs.open(path, 'r', encoding='utf-16-le') as log:
                try:
                    log.seek(index)
                    data += log.readlines()
                except Exception as ex:
                    print('Error reading file: ', ex)

                self.files[path] = log.tell()

        return data


class ChatReader(object):
    def __init__(self, prefixes, path):
        self.eve_client = ''
        self.last_updated = time.time()
        self.observer = Observer()
        self.path = expanduser("~") + path
        patterns = ['*' + x + '*' for x in prefixes]
        self.event_handler = MyHandler(patterns=patterns)

    async def wait_until_ready(self):
        self.observer.schedule(self.event_handler, path=self.path, recursive=False)
        self.observer.start()
        print("waiting for new files")

        while self.event_handler.eve_client == '':
            await asyncio.sleep(3.0)

        self.eve_client = self.event_handler.eve_client
        await asyncio.sleep(3.0)
        self.close()

    async def get_messages(self):
        await asyncio.sleep(5.0)
        raw = self.event_handler.read()
        if raw:
            self.last_updated = time.time()
            raw = [x.replace('\ufeff', '').rstrip() for x in raw if len(x) > 5]  # TODO fix byteorder stuff
            print()
            return raw

        print('.', end='', flush=True)
        return []

    def close(self):
        self.observer.stop()
        self.observer.join()

if __name__ == '__main__':
    c = ChatReader(["The Drone Den"], '\Documents\EVE\logs\Chatlogs')

    async def hmm():
        await c.wait_until_ready()
        while True:
            print(await c.get_messages())

    event_loop = asyncio.get_event_loop()
    b = asyncio.ensure_future(hmm())
    event_loop.run_until_complete(b)
    event_loop.close()
