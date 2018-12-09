import os

from flask import Flask, render_template, request, redirect

from scroll import Twitter_scroll

app = Flask(__name__)


class TweetQuery:
    def __init__(self, query="", faves="", retweets="", since="", until="", lang="", media="", within="", from_="",
                 to_="", geocode="", verified=""):
        self.query = query
        self.faves = faves
        self.retweets = retweets
        self.since = since
        self.until = until
        self.lang = lang
        self.media = media
        self.within = within
        self.from_ = from_
        self.to_ = to_
        self.geocode = geocode
        self.verified = verified

    def join_query(self):
        if self.faves != "0":
            self.query += " min_faves:" + self.faves
        if self.retweets != "0":
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
        if self.geocode != "":
            self.query += " geocode:" + self.geocode
        if self.verified != "":
            self.query = " filter:verified"

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
                           since=request.form["since"], until=request.form["until"], media=request.form["media"],
                           lang=request.form["lang"], verified=request.form["verified"]).join_query()

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
                           media=request.form["media"], lang=request.form["lang"]).join_query()

        return redirect(f"/search/{query}")


@app.route("/scroll", methods=["GET"])
def scroll():
    global search_result, results
    results.scroll()
    search_result = results.tweets

    print(len(search_result))
    return redirect(f"/search/{results.query}")


#
# from flask.ext.sqlalchemy import Pagination

# @app.route('/search/<query>', defaults={'page': 1})
# @app.route('/search/<query>/<int:page>')
# def user_index(page):
#     per_page = 20
#
#     name = request.args.get('name', '')
#     p = User.query.filter((User.name.like('%' + name + '%')) | (not name)).\
#         order_by(User.username.asc()).paginate(page,perpage)
#
#     return render_template( 'user.html', pagination=p,name=name)



if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
