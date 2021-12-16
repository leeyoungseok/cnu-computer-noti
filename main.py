from crawler import Crawler
from Notification import Notification
from Slackbot import Slackbot
from configs import *

def run(bot):
    err_count = 0
    while True:
        is_changed = False
        # 각 url에서
        for url_data in config['NOTIFICATION']['CSE']:
            crawler = Crawler(url_data)
            title = url_data['title']
            url = url_data['url']
            new_data = crawler.crawl_new_notices()  # new 글 읽어서

            if type(new_data) != list:  # 에러나면 string
                bot.send_message(title, new_data)  # 에러 메세지 보낸다
                err_count += 1
                if err_count > 2:
                    bot.send_message(title, "에러가 발생하여 서버 종료합니다")  # 에러 메세지 보낸다
                    return  # 3번 연속 에러나면 종료
                continue
            else:
                err_count = 0  # 정상진행되면 에러 카운트 초기화

            # 저장된 내용이랑 비교
            idxs = notification.get_new_notices(new_data, title)
            if len(idxs) > 0:  # 저장하고 data update
                is_changed = True
                notification.data[title] = new_data  # data update
                # bot.send_message(title, '{}에 새로운 글이 등록되었습니다'.format(title))
                for i in idxs:
                    msg = notification.get_msg(title, url, i)
                    bot.send_message(title, msg)

        if is_changed:  # 새로운 글이 올라왔다면 저장되어있던 공지 update
            notification.save_recents()
        else:
            bot.send_message('TEST', "새로 등록된 글이 없습니다")

        waiting(bot)


if __name__ == '__main__':
    config = get_config()
    bot = Slackbot(config['SLACK'])
    notification = Notification(config['NOTIFICATION'])
    run(bot)
