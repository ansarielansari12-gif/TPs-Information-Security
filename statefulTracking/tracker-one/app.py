from flask import Flask, render_template, request, make_response
import secrets
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "tracker_log.jsonl"


@app.route("/tracker")
def tracker():

    # Check whether the browser already has an identifier
    aid = request.cookies.get("aid")

    # Create a new identifier for a new browser
    if aid is None:
        aid = secrets.token_hex(16)

    # Get information about the page that loaded the tracker
    publisher = request.args.get("publisher", "unknown")
    page = request.args.get("page", "unknown")

    # Record the request
    record = {
        "timestamp": datetime.now().isoformat(),
        "aid": aid,
        "publisher": publisher,
        "page": page
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    # Return the tracker page
    response = make_response(render_template("tracker.html"))

    # Store the identifier in the browser
    if request.cookies.get("aid") is None:
        response.set_cookie(
            key="aid",
            value=aid,
            max_age=60 * 60 * 24 * 365
        )

    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8003, debug=True)