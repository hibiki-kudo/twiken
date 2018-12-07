import random

import requests

from tweet import Tweet

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST)}
BASE_URI = "https://twitter.com/i/search/timeline"


class Twitter_scroll:

    def __init__(self):
        self.pos = ""
        self.lang = ""
        self.query = ""
        self.tweets = []

    def search(self, query):
        self.query = query.replace(' ', '%20').replace('#', '%23').replace(':', '%3A')

        html = requests.get(url=BASE_URI, params={"q": self.query,
                                                  "vertical": "default",
                                                  "max_position": self.pos,
                                                  "src": "typd",
                                                  "include_entities": "1",
                                                  "include_available_features": "1",
                                                  "lang": self.lang
                                                  }, headers=HEADER)

        self.pos = html.json()["min_position"]
        self.tweets = list(Tweet.from_html(html.json()["items_html"]))

        # for tweet in tweets:
        #     print(tweet.user)
        #     print(tweet.icon)
        #     print(tweet.text)

    def scroll(self):
        try:
            html = requests.get(url=BASE_URI, params={"q": self.query,
                                                      "vertical": "default",
                                                      "max_position": self.pos,
                                                      "src": "typd",
                                                      "include_entities": "1",
                                                      "include_available_features": "1",
                                                      "lang": self.lang
                                                      }, headers=HEADER)

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
    twitter.scroll()
    for tweet in twitter.tweets:
        print(f"================================{counter}回目=========================")
        print(tweet.user)
        print(tweet.icon)
        print(tweet.text)
        counter += 1
