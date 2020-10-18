from datetime import datetime
import redis
import json
#
# ts = datetime.fromtimestamp(1602893471980 /1e3)
# print(ts)
#
# b = datetime.fromtimestamp(1601582340)
# print(b)

r = redis.Redis(host='178.128.26.135', port=6379)
a = r.get('upbit:data:btc').decode('utf-8')
print(a)
print(type(json.loads(a)))