import redis

# r = redis.from_url('redis://localhost:6379/0')
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
print(r.get("a201ba69-583d-4d54-b53d-d1ea04a11516"))