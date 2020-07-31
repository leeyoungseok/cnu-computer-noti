from bs4 import BeautifulSoup
import requests


class Crawler:

    def __init__(self, url_data):
        self.title, self.url = url_data['title'], url_data['url']

    def prettier_content(self, str):
        content = str[:-6].strip()
        if content[-1] == '-':
            content = content[:-1].strip()
        # content += '\n\n'
        return content

    def check(self):
        ret = []
        err_msg = ''
        try:
            res = requests.get(self.url)
            soup = BeautifulSoup(res.text, 'html.parser')
            # new가 붙은 공지만 확인 (없을 수도 있다)
            articles = soup.find_all("p", {"class": "b-new"})

            for article in articles:
                date = article.parent.parent.parent.parent.td.find_next("td").find_next("span", {
                    "class": "b-date"}).text.strip()
                title = self.prettier_content(article.parent.parent.a['title'])
                link = article.parent.parent.a['href']
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


if __name__ == "__main__":
    # TEST #
    data = [
        {
            "title": "학사공지",
            "url": "https://computer.cnu.ac.kr/computer/notice/bachelor.do"
        },
        {
            "title": "일반공지",
            "url": "https://computer.cnu.ac.kr/computer/notice/notice.do"
        },
        {
            "title": "사업단공지",
            "url": "https://computer.cnu.ac.kr/computer/notice/project.do"
        }
    ]
    crawler = Crawler(data[2])
    print(crawler.check())
