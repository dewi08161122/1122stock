from infrastructure.redis import get_redis
import json

class dayModel:
    @staticmethod
    def get_TAIEX_information_today(cursor):
        cache_key = "today_TAIEX"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, change_price as change_price,(change_price / (close_price - change_price) * 100) as percent ,trade_value as value FROM TAIEX_prices ORDER BY trade_date DESC LIMIT 1")
            result = cursor.fetchone()
            result["time"]=str(result["time"])
            result["open"]=float(result["open"])
            result["high"]=float(result["high"])
            result["low"]=float(result["low"])
            result["close"]=float(result["close"])
            result["change_price"]=float(result["change_price"])
            result["percent"]=float(result["percent"])
            result["value"]=int(result["value"])
            if result:
                try:
                    redis.setex(cache_key, 60*60*24, json.dumps(result))
                except Exception as e:
                    print(f"Redis Cache Set Error: {e}")
            return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_TPEX_information_today(cursor):
        cache_key = "today_TPEX"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, change_price as change_price,(change_price / (close_price - change_price) * 100) as percent , trade_value as value FROM TPEX_prices ORDER BY trade_date DESC LIMIT 1")
            result = cursor.fetchone()
            result["time"]=str(result["time"])
            result["open"]=float(result["open"])
            result["high"]=float(result["high"])
            result["low"]=float(result["low"])
            result["close"]=float(result["close"])
            result["change_price"]=float(result["change_price"])
            result["percent"]=float(result["percent"])
            result["value"]=int(result["value"])
            if result:
                try:
                    redis.setex(cache_key, 60*60*24, json.dumps(result))
                except Exception as e:
                    print(f"Redis Cache Set Error: {e}")
            return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_market_today(cursor,date: str,market_type: str):
        cache_key = f"today_{market_type}_market"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            cursor.execute("SELECT SUM(change_price > 0) AS rise, SUM(change_price < 0) AS fall, SUM(change_price = 0) AS flat FROM stock_prices STRAIGHT_JOIN stock_name ON stock_prices.number = stock_name.number WHERE trade_date=%s and market_type=%s",[date,market_type])
            result = cursor.fetchone() or {}
            data = {"rise": int(result.get("rise") or 0), "fall": int(result.get("fall") or 0), "flat": int(result.get("flat") or 0)}
            if data:
                try:
                    redis.setex(cache_key, 60*60*24, json.dumps(data))
                except Exception as e:
                    print(f"Redis Cache Set Error: {e}")
        except Exception as e:
            print(e)