import json
import time
from datetime import datetime, timedelta

def get_config():
    with open('config.json') as f:
        config = json.load(f)
    return config

def waiting(bot):
    now = datetime.utcnow() + timedelta(hours=9)

    bot.send_message('TEST', "%s년 %s월 %s일 %s시 %s분" % (
        now.year, now.month, now.day, now.hour, now.minute))
    if now.weekday() >= 5:  # 주말에는 12시간 sleep
        time.sleep(12 * 3600)
    elif not (6 < now.hour < 19):  # 오전 6시 ~ 오후 7시 사이가 아니면
        time.sleep(6 * 3600)  # 6시간 sleep
    else:  # 근무시간이면 INTERVAL_MINS 만큼 sleep
        time.sleep(360)