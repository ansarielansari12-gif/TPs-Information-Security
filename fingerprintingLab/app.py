from flask import Flask, render_template, request

app = Flask(__name__)


# ======================================
# HOME PAGE
# ======================================

@app.route("/")
def home():

    print("\n========== NEW VISIT ==========")

    # ------------------------------
    # Basic HTTP information
    # ------------------------------

    print("IP address        :", request.remote_addr)
    print("HTTP method       :", request.method)

    # ------------------------------
    # Browser information
    # ------------------------------

    print("User-Agent        :", request.headers.get("User-Agent"))
    print("Accept-Language   :", request.headers.get("Accept-Language"))
    print("Accept            :", request.headers.get("Accept"))
    print("Accept-Encoding   :", request.headers.get("Accept-Encoding"))

    # ------------------------------
    # Client Hints
    # ------------------------------

    print("Sec-CH-UA         :", request.headers.get("Sec-CH-UA"))
    print("Sec-CH-UA-Mobile  :", request.headers.get("Sec-CH-UA-Mobile"))
    print("Sec-CH-UA-Platform:", request.headers.get("Sec-CH-UA-Platform"))

    # ------------------------------
    # Fetch Metadata
    # ------------------------------

    print("Sec-Fetch-Site    :", request.headers.get("Sec-Fetch-Site"))
    print("Sec-Fetch-Mode    :", request.headers.get("Sec-Fetch-Mode"))
    print("Sec-Fetch-Dest    :", request.headers.get("Sec-Fetch-Dest"))

    print("================================\n")

    return render_template("index.html")


# ======================================
# COLLECT DATA FROM JAVASCRIPT
# ======================================

@app.route("/collect", methods=["POST"])
def collect():

    # Get JSON data sent by JavaScript
    data = request.get_json()

    # Safety check in case no JSON was received
    if data is None:

        print("\n========== ERROR ==========")
        print("No JSON data received.")
        print("===========================\n")

        return {
            "status": "error",
            "message": "No JSON data received"
        }, 400


    # ======================================
    # PART 2 — ACTIVE BROWSER FEATURES
    # ======================================

    if "browserLanguage" in data:

        print("\n========== ACTIVE FEATURES ==========")

        print(
            "Browser language   :",
            data.get("browserLanguage")
        )

        print(
            "Time zone          :",
            data.get("timeZone")
        )

        print(
            "Screen resolution  :",
            data.get("screenResolution")
        )

        print(
            "Color depth        :",
            data.get("colorDepth")
        )

        print(
            "Logical CPU cores  :",
            data.get("cpuCores")
        )

        print(
            "Browser window size:",
            data.get("windowSize")
        )

        print("=====================================\n")


    # ======================================
    # TASK 4 — ALICE'S TYPING RHYTHM
    # ======================================

    if "typingTime" in data:

        print("\n========== TYPING BEHAVIOUR ==========")

        print(
            "Typing time        :",
            data.get("typingTime"),
            "seconds"
        )

        print(
            "Typing speed       :",
            data.get("typingSpeed"),
            "characters/second"
        )

        print(
            "Corrections        :",
            data.get("corrections")
        )

        print("======================================\n")


    # ======================================
    # PART 4 — SHA-256 FINGERPRINT
    # ======================================

    if "fingerprint" in data:

        print("\n========== FINGERPRINT ==========")

        print(
            "SHA-256 fingerprint:",
            data.get("fingerprint")
        )

        print("=================================\n")


    # ======================================
    # SERVER RESPONSE
    # ======================================

    return {
        "status": "received"
    }


# ======================================
# START FLASK SERVER
# ======================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=True
    )