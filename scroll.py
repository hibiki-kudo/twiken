import random

import requests
from bs4 import BeautifulSoup

from tweet import Tweet

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST)}


# BASE_URI = "https://twitter.com/i/search/timeline"


class Twitter_scroll:

    def __init__(self):
        self.pos = ""
        self.query = ""
        self.tweets = []
        self.lang = ""
        self.BASE_URI = '''https://twitter.com/search?f=tweets&vertical=default&q={query}&l={lang}'''
        self.RELOAD_URI = '''https://twitter.com/i/search/timeline?f=tweets&vertical=default&include_available_features=1&include_entities=1&reset_error_state=false&src=typd&max_position={pos}&q={query}&l={lang}'''

    def search(self, query):
        self.query = query.replace(' ', '%20').replace('#', '%23').replace(':', '%3A')
        self.pos = ""
        print(self.query)
        print(self.pos)

        html = requests.get(url=self.BASE_URI.format(query=self.query, lang=self.lang), headers=HEADER)

        self.tweets = list(Tweet.from_html(html.text))  # .json()["items_html"]))
        try:
            self.pos = BeautifulSoup(html.text, "html.parser").find("div", attrs={"class": "stream-container "})[
            "data-min-position"]
        except:
            pass
        print(len(self.tweets))

        # for tweet in tweets:
        #     print(tweet.user)
        #     print(tweet.icon)
        #     print(tweet.text)

    def scroll(self):
        try:
            html = requests.get(url=self.RELOAD_URI, headers=HEADER)

            self.tweets = list(Tweet.from_html(html.json()["items_html"]))
            self.pos = html.json()["min_position"]
            # print(html.text)
            return

        except:
            print("これ以上見つけられないよ")
            return "これ以上は見つけられないよ"


if __name__ == "__main__":
    twitter = Twitter_scroll()
    twitter.search("python")
    counter = 1

    for tweet in twitter.tweets:
        print(f"================================{counter}回目=========================")
        print(tweet.user)
        print(tweet.icon)
        print(tweet.text)
        counter += 1

    counter = 1
    for i in range(5):
        twitter.scroll()
        for tweet in twitter.tweets:
            print(f"================================{counter}回目=========================")
            print(tweet.user)
            print(tweet.icon)
            print(tweet.text)
            counter += 1
