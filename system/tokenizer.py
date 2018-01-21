from datetime import datetime
import re

from esi.common import universe_names_to_ids


class Message:
    def __init__(self, message):
        print(message)
        self.raw_text = message  # for debug only
        self.timestamp = datetime.strptime(message[2:21], '%Y.%m.%d %H:%M:%S')
        self.sender = message[message.find(']')+2:message.find('>')-1]
        self.message = message[message.find('>')+2:]
        self.tokens = []

    async def tokenize(self, stop_words):
        """
        Figures out the best parse of a string
        :param message: raw string to convert into tokens
        :return:list of (tokentype, string)
        """
        raw_tokens = re.sub("\s\s+", " ", self.message).split()

        query = []
        for i in range(len(raw_tokens)):
            for j in range(1, min(4, len(raw_tokens) - i + 1)):
                query.append(' '.join(raw_tokens[i: i + j]))

        result = await universe_names_to_ids(query)

        tokens = []
        index = 0

        # print(self.raw_text)
        return query

    @classmethod
    async def new(cls, message, stop_words=None):
        obj = cls(message)
        obj.tokens = await obj.tokenize(stop_words)
        return obj

    def __str__(self):
        return str(self.timestamp) + '\nSender: ' + self.sender + '\nMessage: ' + self.message


# todo test empty message