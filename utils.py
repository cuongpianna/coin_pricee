import redis
import json
r = redis.Redis(host='178.128.26.135', port=6379)

def get_current_code():
    flag = r.exists('currency')
    if flag == 0:
        r.set('currency', 'btc')

    current_code = r.get('currency').decode('utf-8')
    return current_code