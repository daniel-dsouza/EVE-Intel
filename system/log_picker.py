from os.path import expanduser, getctime
import glob


LOG_DIR = expanduser('~\\Downloads')  # 'C:\\Users\\danie\\Downloads'


def most_recent_logs(channels):
    def get_latest_log(channel):
        log_files = glob.glob('{}\\{}*.txt'.format(LOG_DIR, channel))
        return max(log_files, key=getctime)

    return [get_latest_log(c) for c in channels]


# print(most_recent_logs(['The Drone Den']))
