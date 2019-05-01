from flask import Flask
from flask import jsonify
import json

app = Flask(__name__)


@app.route('/bonds')
def list_bonds():

    with open("bonds.json") as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/trades')
def list_trades():

    with open("trades.json") as f:
        data = json.load(f)

    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555, debug=True)
