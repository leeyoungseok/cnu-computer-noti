from crawler import *
from csenoti_slack_bot import *
import time
from datetime import datetime, timedelta

config = getConfig()
bot = CSEbot(config['SLACK'])
notification = CSEnotification(config['NOTIFICATION'])


def run():
    err_count = 0
    while True:
        is_changed = False
        # 각 url에서
        for url_data in config['NOTIFICATION']['CSE']:
            crawler = Crawler(url_data)
            title = url_data['title']
            new_data = crawler.check()  # new 글 읽어서

            if type(new_data) != list:  # 에러나면 string
                bot.sendMessage(title, new_data)  # 에러 메세지 보낸다
                err_count += 1
                if err_count > 2:
                    bot.sendMessage(title, "에러가 발생하여 서버 종료합니다")  # 에러 메세지 보낸다
                    return  # 3번 연속 에러나면 종료
                continue
            else:
                err_count = 0  # 정상진행되면 에러 카운트 초기화

            # 저장된 내용이랑 비교
            idxs = notification.isDiff(new_data, title)
            if len(idxs) > 0:  # 저장하고 data update
                is_changed = True
                notification.data[title] = new_data  # data update
                # bot.sendMessage(title, '{}에 새로운 글이 등록되었습니다'.format(title))
                for i in idxs:
                    msg = notification.get_msg(title, i)
                    bot.sendMessage(title, msg)

        if is_changed:  # 새로운 글이 올라왔다면 저장되어있던 공지 update
            notification.save_recents()
        else:
            bot.sendMessage('TEST', "새로 등록된 글이 없습니다")

        waiting()

def waiting():
    now = datetime.utcnow() + timedelta(hours=9)

    bot.sendMessage('TEST', "%s년 %s월 %s일 %s시 %s분" % (
        now.year, now.month, now.day, now.hour, now.minute))
    if now.weekday() < 5:  # 평일에는 12시간 sleep
        time.sleep(12 * 3600)
    elif not (6 < now.hour < 19):  # 오전 6시 ~ 오후 7시 사이가 아니면
        time.sleep(6 * 3600)  # 6시간 sleep
    else:  # 근무시간이면 30분에 한번씩
        time.sleep(config['INTERTAL_MINS']*60)

if __name__ == '__main__':
    run()
