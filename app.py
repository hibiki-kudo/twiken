from flask import Flask, render_template, request, redirect

from scroll import Twitter_scroll

app = Flask(__name__)

search_result = []
results = Twitter_scroll()


@app.route("/", methods=["GET", "POST"])
def index():
    global search_result, results
    if request.method == "GET":
        return render_template("sample.html")

    if request.method == "POST":
        search_result.clear()
        query = request.form["keyword"]
        results.search(query)
        search_result = results.tweets
        with open("query.txt", "w") as f:
            for tweet in search_result:
                f.write(
                    f"{tweet.fullname},,,,,,{tweet.user},,,,,,{tweet.icon},,,,,,{tweet.text},,,,,,{tweet.timestamp}\n\n\n\n----")
        return redirect(f"/result/{query}")


@app.route("/result/<query>", methods=["GET", "POST"])
def result(query):
    global search_result
    if request.method == "GET":
        with open("query.txt", "r") as f:
            search_list = f.read().split("\n\n\n\n----")

        print(len(search_list))

        for tweet in search_list:
            search_result.append(tweet.split(",,,,,,"))

        print(search_result)
        return render_template("sample.html", results=search_result)

    if request.method == "POST":
        search_result.clear()
        query = request.form["keyword"]
        results.search(query)
        search_result = results.tweets
        with open("query.txt", "w") as f:
            for tweet in search_result:
                f.write(
                    f"{tweet.fullname},,,,,,{tweet.user},,,,,,{tweet.icon},,,,,,{tweet.text},,,,,,{tweet.timestamp}\n\n\n\n----")
        return redirect(f"/result/{query}")


@app.route("/scroll", methods=["GET"])
def scroll():
    global search_result, results
    results.scroll()
    search_result = results.tweets
    with open("query.txt", "a") as f:
        for tweet in search_result:
            f.write(
                f"{tweet.fullname},,,,,,{tweet.user},,,,,,{tweet.icon},,,,,,{tweet.text},,,,,,{tweet.timestamp}\n\n\n\n----")

    print(len(search_result))
    return redirect(f"/result/{results.query}")


if __name__ == "__main__":
    app.run(debug=True)
