from slacker import Slacker


class Slackbot:
    def __init__(self, config):
        token = config['TOKEN']
        self.channels = config['CHANNELS']  # TEST, BACHELOR, NOTICE, PROJECT
        self.bot = Slacker(token)

    def send_message(self, channel_title, msg):
        if channel_title == "학사공지":
            channel = self.channels['BACHELOR']
        elif channel_title == "일반공지":
            channel = self.channels['NOTICE']
        elif channel_title == "사업단공지":
            channel = self.channels['PROJECT']
        else:
            channel = self.channels['TEST']
        # 메시지 전송 (#채널명, 내용)
        self.bot.chat.post_message(channel, msg)