from flask import Flask
from flask import jsonify

app = Flask(__name__)

BONDS = [
    {"a":1},
    {"b":2}
]

@app.route('/bonds')
def list_bonds():
    return jsonify(BONDS)


if __name__ == '__main__':
    app.run(port=5555)