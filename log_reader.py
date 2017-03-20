import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from os.path import expanduser
import codecs
import itertools

# anomaly_regex = re.compile("[A-Z0-9][A-Z0-9][A-Z0-9]")
observer = Observer()


def start_observer():
    observer.start()
    print("waiting for new files")


class MyHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        print("found {}".format(event.src_path))
        time.sleep(0.1)  # if there is no delay, then you may not be able to open the file!
        with codecs.open(event.src_path, 'r', 'utf-16-le') as log:
            _ = log.readlines()
            # print(a)
            self.files[event.src_path] = log.tell()


class LogReader(object):
    def __init__(self, prefixes, path):
        self.path = expanduser("~") + path
        self.patterns = ['*' + x + '*' for x in prefixes]

        self.event_handler = MyHandler(patterns=self.patterns)
        self.event_handler.files = {}
        observer.schedule(self.event_handler, path=self.path, recursive=False)

    def read_logs(self):
        for path, index in self.event_handler.files.items():
            with codecs.open(path, 'r', 'utf-16-le') as log:
                log.seek(index)
                data = log.readlines()
                self.event_handler.files[path] = log.tell()

                if data:
                    print(data)  # make custom data structure with words?
                    return data


if __name__ == '__main__':
    o = LogReader(["The Drone Den", "Obliteroids"], '\Documents\EVE\logs\Chatlogs')
    p = LogReader(["oba"], '\Documents\EVE\logs\Chatlogs')
    start_observer()
    try:
        while True:
            print("1: {0}".format(o.read_logs()))
            print("2: {0}".format(p.read_logs()))
            time.sleep(10)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()
