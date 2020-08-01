import json


class Notification:
    def __init__(self, config):
        self.data = None
        self.cse = config['CSE']
        self.path = config['RECENT_FILE']
        self._load_recents()  # data init : 처음 한 번 가지고 오기

    def _load_recents(self):
        with open(self.path, "r", encoding='utf-8') as f:
            self.data = json.load(f)

    def save_recents(self):
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_new_notices(self, arr, url_title):
        # [{"date":..., "title":..., "link":...},...]
        ret = []  # 업데이트된 인덱스들
        for idx, el in enumerate(arr):
            if not any(el['title'] in s['title'] for s in self.data[url_title]):
                ret.append(idx)
        return ret

    def get_msg(self, title, url, idx):
        return '작성일 : {}\n제목 : {}\n링크 : {}'.format(
            self.data[title][idx]['date'],
            self.data[title][idx]['title'],
            url+self.data[title][idx]['link'])
