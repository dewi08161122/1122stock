from infrastructure.connection import get_connection
from infrastructure.redis import get_redis
import json

class SearchModel:
    @staticmethod
    def get_category():
        cache_key = "all_categories"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT category_name FROM stock_category ORDER BY category_number ASC")
                    result = cursor.fetchall()
                    if result:
                        try:
                            redis.set(cache_key, json.dumps(result))
                        except Exception as e:
                            print(f"Redis Cache Set Error: {e}")
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_categorystock(category_name: str):
        cache_key = f"categories:{category_name}"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT number, name FROM stock_name JOIN stock_category ON stock_name.category_number = stock_category.category_number WHERE category_name = %s ORDER BY number ASC",[category_name])
                    result = cursor.fetchall()
                    if result:
                        try:
                            redis.set(cache_key, json.dumps(result))
                        except Exception as e:
                            print(f"Redis Cache Set Error: {e}")
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def search_stock(keyword: str):
        keyword = keyword.strip()
        cache_key = f"keyword:{keyword}"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            search = f"{keyword}%"
            sql = """
                SELECT number, name 
                FROM stock_name 
                WHERE number LIKE %s OR name LIKE %s 
                ORDER BY 
                (number = %s) DESC,
                (number LIKE %s) DESC,
                (name LIKE %s) DESC 
                LIMIT 10
            """
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute(sql, [
                        search, search, 
                        keyword, search, search
                    ])
                    result = cursor.fetchall()
                    if result:
                        try:
                            redis.set(cache_key, json.dumps(result))
                        except Exception as e:
                            print(f"Redis Cache Set Error: {e}")
                    return result
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def get_trade_value_ranking(trade_date: str):
        cache_key = "today_trade_value_ranking"
        redis = get_redis()
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis Cache Get Error: {e}")
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT trade_date as time,open_price as open, high_price as high, low_price as low, close_price as close, change_price as change_price,(change_price / (close_price - change_price) * 100) as percent, stock_prices.number, name FROM stock_prices JOIN stock_name ON stock_prices.number = stock_name.number WHERE trade_date = %s ORDER BY trade_value DESC LIMIT 30",[trade_date])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["change_price"]=float(i["change_price"])
                        i["percent"]=float(i["percent"])
                    if result:
                        try:
                            redis.setex(cache_key, 60*60*24, json.dumps(result))
                        except Exception as e:
                            print(f"Redis Cache Set Error: {e}")
                    return result
        except Exception as e:
            print(e)