import json
from flask import Flask, request
from redis import Redis

app = Flask(__name__)
try:
    redis = Redis(host="redis", port=6379)
except:
    redis = Redis(host="btree-sr-redis", port=6379)
finally:
    redis = None


@app.route("/")
def hello():
    if not redis:
        return {}
    redis.incr("hits")
    counter = str(redis.get("hits"), "utf-8")
    data = {
        "msg": f"This page has been viewed {counter} time(s)",
        "apis": ["/search?arg=<any airport code>"],
    }
    return data


@app.route("/search")
def search_airport():
    """search airport by iata code"""
    arg = request.args.get("arg")
    if not arg:
        return "give a valid arg", 400
    if not redis:
        return {}
    arg = arg.upper()
    if len(arg) == 3:
        result = redis.get(arg)
    else:
        result = None
    if not result:
        return "result not found", 400
    return [json.loads(str(result, "utf-8"))]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
