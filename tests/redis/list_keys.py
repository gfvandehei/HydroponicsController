import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
for key in r.scan_iter("*"):
    print(key)