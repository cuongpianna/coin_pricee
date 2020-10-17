import redis
import json
r = redis.Redis()

def get_current_code():
    flag = r.exists('currency')
    if flag == 0:
        r.set('currency', 'btc')

    current_code = r.get('currency').decode('utf-8')
    return current_code