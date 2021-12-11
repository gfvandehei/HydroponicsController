import redis
import sys

sysid = int(sys.argv[1])
sensorid = int(sys.argv[2])

r = redis.StrictRedis(host='localhost', port=6379, db=0)
key = f"system:{sysid}:sensor:dhtsensor:{sensorid}"
print(r.xrange(key, min="-", max="+"))