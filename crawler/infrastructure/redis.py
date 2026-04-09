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

def cleanup_after_crawl():
    redis = get_redis()
    all_keys = redis.keys("*")
    
    delete = [i for i in all_keys if "kline" in i or "today" in i]
    if delete:
        redis.delete(*delete)
        print(f"成功清理 Redis 快取，共移除 {len(delete)} 筆資料。")
