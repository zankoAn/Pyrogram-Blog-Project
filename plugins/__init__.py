import redis

query = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
)

admin = your_id
