#from slacker import Slacker
from slack_sdk import WebClient
import requests


class Slackbot:
    def __init__(self, config):
        self.token = config['TOKEN']
        self.channels = config['CHANNELS']  # TEST, BACHELOR, NOTICE, PROJECT
#        self.bot = Slacker(self.token)

    def send_message(self, channel_title, msg):
        channel = self.channels
        token = self.token
        print(channel, ": ", msg)
        # 메시지 전송 (#채널명, 내용)
        #self.bot.chat.post_message(channel, msg)
        response = requests.post('https://slack.com/api/chat.postMessage',
                      headers={'Authorization': 'Bearer '+token}, 
                      #headers={'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}, 
                      data={'channel': channel, 'text': msg})
        print(response.text)
        #client = WebClient(token)
        #response = client.chat_postMessage(channel='#general', text=msg)