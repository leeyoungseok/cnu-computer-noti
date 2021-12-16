from bs4 import BeautifulSoup
import requests


class Crawler:

    def __init__(self, url_data):
        self.title, self.url = url_data['title'], url_data['url']

    def _prettier_title(self, str):
        content = str[:-6].strip()
        if content[-1] == '-':
            content = content[:-1].strip()
        # content += '\n\n'
        return content

    def crawl_new_notices(self):
        ret = []
        err_msg = ''
        try:
            res = requests.get(self.url)
            soup = BeautifulSoup(res.text, 'html.parser')
            # new가 붙은 공지만 확인 (없을 수도 있다)
            articles = soup.find_all("p", {"class": "b-new"})

            for article in articles:
                this_article = article.parent.parent
                date = this_article.parent.parent.td.find_next("td").find_next("span", {
                    "class": "b-date"}).text.strip()
                title = self._prettier_title(this_article.a['title'])
                link = this_article.a['href']
                ret.append({"date": date, "title": title, "link": link})

            return ret

        except requests.exceptions.HTTPError as errh:
            err_msg = "Http Error: " + errh
            print(err_msg)
        except requests.exceptions.ConnectionError as errc:
            err_msg = "Error Connecting: " + errc
            print(err_msg)
        except requests.exceptions.Timeout as errt:
            err_msg = "Timeout Error: " + errt
            print(err_msg)
        except requests.exceptions.RequestException as err:
            err_msg = "OOps: Something Else" + err
            print(err_msg)

        return err_msg