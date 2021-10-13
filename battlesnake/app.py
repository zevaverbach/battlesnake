from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "apiversion": "1",
            "author": "zevaverbach",
            "head": "default",
            "color": "#E1AD01",
            "tail": "default",
            "version": "0.0.1-beta",
        }
    )


@app.route("/start", methods=["POST"])
def start():
    pass


@app.route("/move", methods=["POST"])
def move():
    return jsonify({"move": "up"})


@app.route("/end", methods=["POST"])
def end():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0")
