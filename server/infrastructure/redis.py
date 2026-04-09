import os
import redis

redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    max_connections=30
)

def get_redis():
    return redis.Redis(connection_pool=redis_pool)