from cachetools import TTLCache, LRUCache

KLINE_CACHE = TTLCache(maxsize=1000, ttl=5*60)

CATEGORY_CACHE = LRUCache(maxsize=3000)

INDEXHOTSTOCK_CACHE = TTLCache(maxsize=30, ttl=5*60)

SEARCHSTOCK_CACHE = LRUCache(maxsize=1000)