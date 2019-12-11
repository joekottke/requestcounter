# Simple Request Counter

import threading
from flask import jsonify, Flask


class AtomicCounter(object):

    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1):
        with self._lock:
            self.value += num

    def reset(self, num=0):
        with self._lock:
            self.value = num


counter = AtomicCounter()
app = Flask('requestcounter')


@app.route('/')
def index():
    counter.increment()
    return jsonify({"theanswer": 42})


@app.route('/metrics')
def metrics():
    return jsonify({"theanswer_count": counter.value})


@app.route('/reset')
def reset():
    counter.reset()
    return jsonify({"message": "reset complete"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5555')
