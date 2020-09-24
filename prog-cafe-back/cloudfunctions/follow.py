from flask import jsonify
import redis
import json
import time
url = "redis://h:p67a72fdc9e0b5ff64d97388a2890aad0f232e1345a94014540b23bcdd14f4242@ec2-50-16-12-122.compute-1.amazonaws.com:15169"
r = redis.from_url(url)

# @auther Okada Yuka


def follow(request):
    id = json.loads((request.data.decode()))["id"]
    to = json.loads((request.data.decode()))["to"]
    type = json.loads((request.data.decode()))["type"]
    timestamp = time.time()

    # typeがfollowの場合，following DBのidを追加する
    if type == 'follow':
        r.zadd("following:"+str(id), {to:int(timestamp)})

    # typeがunfollowの場合，follow DBのidを削除する
    else:
        r.zrem("following:"+str(id), to)

    response=jsonify(json.loads('{\"200\":\"succeeded\"}'))
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    return  response
