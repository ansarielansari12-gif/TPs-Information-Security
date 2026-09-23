from flask import Flask, request

app = Flask(__name__)


@app.route("/collect")
def collect():
    analytics_id = request.args.get("id")
    publisher = request.args.get("publisher")
    page = request.args.get("page")

    print("\n--- ANALYTICS REQUEST ---")
    print("ID:", analytics_id)
    print("Publisher:", publisher)
    print("Page:", page)

    return "OK"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9100, debug=True)