# Simple Request Counter

import hashlib
import os
import pathlib
import threading
from quart import jsonify, Quart

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
app = Quart('requestcounter')

buildinfo = {}
for filename in os.listdir('build-info'):
    fh = open('build-info/' + filename) 
    buildinfo[filename] = fh.read().strip()
    fh.close()

@app.route('/')
async def index():
    counter.increment()
    return {"theanswer": 42}


@app.route('/metrics')
async def metrics():
    return {"theanswer_count": counter.value}


@app.route('/reset')
async def reset():
    counter.reset()
    return {"message": "reset complete"}


@app.route('/build-info')
async def build_info():
    return buildinfo

if __name__ == "__main__":
    filepath = pathlib.Path(__file__).absolute()
    contents = open(filepath).read()
    md5hash = hashlib.md5(contents.encode()).hexdigest()
    print(filepath, md5hash)
    port = os.getenv("PORT") if os.getenv("PORT") else '5555'
    app.run(host='0.0.0.0', port=port)
