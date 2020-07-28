import json
from slacker import Slacker


class CSEbot:
    def __init__(self, config):
        token = config['TOKEN']
        self.channels = config['CHANNELS']  # TEST, BACHELOR, NOTICE, PROJECT
        self.bot = Slacker(token)

    def sendMessage(self, channel_title, msg):
        if channel_title == "학사공지":
            channel = self.channels['BACHELOR']
        elif channel_title == "일반공지":
            channel = self.channels['NOTICE']
        elif channel_title == "사업단공지":
            channel = self.channels['PROJECT']
        else:
            channel = self.channels['TEST']
        # print("channel : ",channel)
        # 메시지 전송 (#채널명, 내용)
        channel = self.channels['TEST']
        self.bot.chat.post_message(channel, msg)


class CSEnotification:
    def __init__(self, config):
        self.data = None
        self.config = config
        self.path = config['RECENT_FILE']
        self.load_recents()  # data init : 처음 한 번 가지고 오기

    def load_recents(self):
        with open(self.path, "r", encoding='utf-8') as f:
            self.data = json.load(f)

    def save_recents(self):
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def isDiff(self, arr, url_title):
        # [{"date":..., "title":...},...]
        ret = []  # 업데이트된 인덱스들
        for idx, el in enumerate(arr):
            if not any(el['title'] in s['title'] for s in self.data[url_title]):
                ret.append(idx)
        return ret

    def get_msg(self, title, idx):
        return '작성일 : {}\n제목 : {}\n\n'.format(
            self.data[title][idx]['date'],self.data[title][idx]['title'])


def getConfig():
    with open('config.json') as f:
        config = json.load(f)
    return config
