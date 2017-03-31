import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from os.path import expanduser, basename
import codecs

# anomaly_regex = re.compile("[A-Z0-9][A-Z0-9][A-Z0-9]")
observer = Observer()


def prefix(path):
    return basename(path)[:basename(path).find('_2')]  # will not work after the year 2999


def start_observer():
    observer.start()
    print("waiting for new files")


class MyHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        time.sleep(0.1)  # if there is no delay, then you may not be able to open the file!
        with codecs.open(event.src_path, 'r', 'utf-16') as log:
            if prefix(log.name) not in [prefix(x) for x in self.files]:  # do not read same log from multiple clients
                _ = log.readlines()
                print("using {0} to read '{1}'".format(log.name, prefix(log.name)))
                self.files[event.src_path] = log.tell()
            else:
                print("already reading '{0}'".format(prefix(log.name)))


class LogReader(object):
    def __init__(self, prefixes, path):
        self.path = expanduser("~") + path
        self.patterns = ['*' + x + '*' for x in prefixes]  # match any files that contain the prefix

        self.event_handler = MyHandler(patterns=self.patterns)
        self.event_handler.files = {}
        observer.schedule(self.event_handler, path=self.path, recursive=False)

    def read_logs(self):
        for path, index in self.event_handler.files.items():
            with codecs.open(path, 'r', 'utf-16') as log:
                log.seek(index)
                data = log.readlines()
                self.event_handler.files[path] = log.tell()

                if data:
                    data = [x.replace('\ufeff', '').rstrip() for x in data]  # TODO fix byteorder stuff
                    return data


if __name__ == '__main__':
    # o = LogReader(["The Drone Den", "Obliteroids"], '\Documents\EVE\logs\Chatlogs')
    p = LogReader(["oba"], '\Documents\EVE\logs\Chatlogs')
    start_observer()
    try:
        while True:
            # print("1: {0}".format(o.read_logs()))
            print("2: {0}".format(p.read_logs()))
            time.sleep(10)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
