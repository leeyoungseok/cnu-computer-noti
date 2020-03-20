import time

import telegram
from computer import Computer
import json
from datetime import datetime, timedelta

data = None  # dict
# {
#   "학사공지" : [],
#   "일반공지" : [],
#   "사업단공지" :  []
# }


def load_notices(path):
    global data
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)


def save_notices(path):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_latest_json():
    # recents.json에서 가장 최신인 것
    global data
    arrs = [data['bachelor'], data['notice'], data['project']]
    ret = []
    for arr in arrs:
        if len(arr) == 0:
            ret.append('')
        else:
            ret.append(arr[0]['title'])


def get_latest_web(computer, url):
    global data


def isDiff(arr, url_title):
    # [{"date":..., "title":...},...]
    ret = []  # 업데이트된 인덱스들
    for idx, el in enumerate(arr):
        if not any(el['title'] in s['title'] for s in data[url_title]):
            ret.append(idx)
    return ret


def main(config):
    global data
    token = config['TELEGRAM']['TOKEN']
    bot = telegram.Bot(token)
    computer = Computer(config['urls']['computer'])
    recent_file = "recents.json"

    bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'], '충남대학교 공지사항 알리미를 시작합니다')

    # data init : 처음 한 번 가지고 오기
    load_notices(recent_file)

    while True:
        is_changed = False
        # 각 url에서
        for url_data in config['urls']['computer']:
            arr = computer.check_noti(url_data)  # new 글 읽어서
            if type(arr) != list:  # 에러나면 string
                bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'], arr)
                continue
            url_title = url_data['title']
            # 저장된 내용이랑 비교
            idxs = isDiff(arr, url_title)
#             print('{}의 다른 인덱스 : {}'.format(url_title, idxs))
            if len(idxs) > 0:  # 저장하고 data update
                is_changed = True
                data[url_title] = arr  # data update
                bot.sendMessage(
                    config['TELEGRAM']['COMPUTER_NOTI_CHANNEL'], '{}에 새로운 글이 등록되었습니다'.format(url_title))
                for i in idxs:
                    msg = '작성일 : {}\n제목 : {}\n\n'.format(
                        data[url_title][i]['date'], data[url_title][i]['title'])
                    bot.sendMessage(config['TELEGRAM']
                                    ['COMPUTER_NOTI_CHANNEL'], msg)

        now = datetime.utcnow() + timedelta(hours=9)
        if is_changed:
            save_notices(recent_file)  # 저장
#         else:
#             bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'],"새로 등록된 글이 없습니다")

        bot.sendMessage(config['TELEGRAM']['RECEIVER_ID'], "%s년 %s월 %s일 %s시 %s분" % (
            now.year, now.month, now.day, now.hour, now.minute))
        if not (6 < now.hour < 19):  # 오전 6시 ~ 오후 7시 사이가 아니면
            time.sleep(6 * 3600)  # 6시간 sleep
        else:  # 근무시간이면 30분에 한번씩
            time.sleep(config['INTERTAL_MINS']*60)


if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)
    main(config)
