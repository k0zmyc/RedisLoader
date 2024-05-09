import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)



#######################################################################
########################  Insert data as JSON  ########################
#######################################################################


def load_db(key, items):
    
    r.flushall

    for item in items:
        item_id = item['id']
        #Data converion
        item_json = json.dumps(item)
        #Store as JSON using predefined RedisJSON
        #r.json().set('data', '$', item)
        item_key = f"{key}:{item_id}"  # Append item ID to key
        r.execute_command('JSON.SET', item_key, '.', item_json)
# Load JSON data with UTF-8 encoding
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

# Insert data for each instance dynamically
for key, value in data.items():
    load_db(key, value)
