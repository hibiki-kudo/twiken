from flask import Flask, render_template, request, redirect

from scroll import Twitter_scroll

app = Flask(__name__)


class TweetQuery:
    def __init__(self, query="", faves="", retweets="", since="", until="", lang="", media="", from_="", to_=""):
        self.query = query
        self.faves = faves
        self.retweets = retweets
        self.since = since
        self.until = until
        self.lang = lang
        self.media = media
        self.from_ = from_
        self.to_ = to_

    def join_query(self):
        if self.faves != "":
            self.query += " min_faves:" + self.faves
        if self.retweets != "":
            self.query += " min_retweets:" + self.retweets
        if self.since != "":
            self.query += " since:" + self.since
        if self.until != "":
            self.query += " until:" + self.until
        if self.lang != "":
            self.query += " lang:" + self.lang
        if self.media != "":
            self.query += " filter:" + self.media
        if self.from_ != "":
            self.query += " from:" + self.from_
        if self.to_ != "":
            self.query += " to:" + self.to_

        return self.query


search_result = []
results = Twitter_scroll()


@app.route("/search/", methods=["GET", "POST"])
def index():
    global search_result, results

    if request.method == "GET":
        return render_template("twiken.html")

    if request.method == "POST":
        search_result.clear()
        query = TweetQuery(query=request.form["keyword"], faves=request.form["favorite"], retweets=request.form["RT"],
                           since=request.form["since"], media=request.form["media"]).join_query()

        print(query)
        print(request.form["since"])
        return redirect(f"/search/{query}")


@app.route("/search/<query>", methods=["GET", "POST"])
def result(query):
    global search_result, results

    if request.method == "GET":
        if query == "":
            return render_template("twiken.html")

        results.search(query)
        search_result = results.tweets
        return render_template("twiken.html", results=search_result,
                               query=query.replace('%20', ' ').replace('%23', '#').replace('%3A', ':'))

    if request.method == "POST":
        search_result.clear()
        query = TweetQuery(query=request.form["keyword"], faves=request.form["favorite"],
                           retweets=request.form["RT"], since=request.form["since"],
                           media=request.form["media"]).join_query()

        return redirect(f"/search/{query}")


@app.route("/scroll", methods=["GET"])
def scroll():
    global search_result, results
    results.scroll()
    search_result = results.tweets

    print(len(search_result))
    return redirect(f"/search/{results.query}")


if __name__ == "__main__":
    app.run(debug=True)
