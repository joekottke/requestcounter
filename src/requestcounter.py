# Simple Request Counter

import grpc
import hashlib
import os
import pathlib
import random
import threading
from quart import jsonify, Quart

import gubernator_pb2
import gubernator_pb2_grpc

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

rate_limit_request = gubernator_pb2.RateLimitReq(
    name="request_per_second",
    unique_key="global",
    hits=1,
    limit=1,
    duration=1000
)

gubernator_host = "gubernator"
gubernator_port = 5555

accepted_counter = AtomicCounter()
denied_counter = AtomicCounter()
app = Quart('requestcounter')

buildinfo = {}
for filename in os.listdir('build-info'):
    fh = open('build-info/' + filename) 
    buildinfo[filename] = fh.read().strip()
    fh.close()

def is_permitted(key):
    return bool(random.randint(0,1))

@app.route('/')
async def index():
    resp = {"theanswer": 42}
    if is_permitted("ip:127.0.0.1"):
        accepted_counter.increment()
    else:
        denied_counter.increment()
        resp = {"error": "Too Many Requests"}
    return resp

@app.route('/metrics')
async def metrics():
    return {
        "count_accepted": accepted_counter.value,
        "count_denied": denied_counter.value
    }

@app.route('/reset')
async def reset():
    accepted_counter.reset()
    denied_counter.reset()
    return {"message": "reset complete"}

@app.route('/build-info')
async def build_info():
    return buildinfo

def main():
    filepath = pathlib.Path(__file__).absolute()
    contents = open(filepath).read()
    md5hash = hashlib.md5(contents.encode()).hexdigest()
    print(filepath, md5hash)
    port = os.getenv("PORT", 5555)
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()