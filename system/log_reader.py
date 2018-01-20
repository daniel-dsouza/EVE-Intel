import codecs
from datetime import datetime
import re


class Message:
    def __init__(self, message):
        self.raw = message  # for debug only
        self.timestamp = datetime.strptime(message[2:21], '%Y.%m.%d %H:%M:%S')
        self.sender = message[message.find(']')+2:message.find('>')-1]
        self.message = message[message.find('>')+2:]

    def __str__(self):
        return str(self.timestamp) + '\nSender: ' + self.sender + '\nMessage: ' + self.message


class ChannelReader:
    def __init__(self, filepath):
        self._filepath = filepath
        self._read_index = 0
        self._client = ''
        self._MOTD = ''  # not implemented

        with codecs.open(self._filepath, 'r', encoding='utf-16-le') as log:
            lines = log.readlines()
            self._client = re.sub("\s\s+", " ", lines[8]).split(': ')[1]
            self._read_index = log.tell()

    def get_motd(self):
        """Get the Message of the Day from the current channel"""
        return self._MOTD

    def get_filename(self):
        """Get the filename of the current channel log"""
        print(self._filepath)
        return self._filepath[self._filepath.rindex('\\')+1:]

    def get_eve_client(self):
        return self._client

    def read_messages(self):
        with codecs.open(self._filepath, 'r', encoding='utf-16-le') as log:
            try:
                log.seek(self._read_index)
                lines = [x.replace('\ufeff', '').rstrip() for x in log.readlines() if len(x) > 5]
                self._read_index = log.tell()
            except Exception as ex:
                print('Error reading file: ', ex)

        if lines is None:
            return []

        return [Message(line) for line in lines]


# from log_picker import most_recent_logs
# log = most_recent_logs(['The Drone Den'])
# chan = ChannelReader(log[0])
# # print(chan.get_filename())
# # print(chan.get_eve_client())
#
# import time
# time.sleep(5)
#
# for m in chan.read_messages():
#     print(m)
