from infrastructure.connection import get_connection
from infrastructure.cache import KLINE_CACHE

class KLineModel:
    @staticmethod
    def get_stock_KLine(stockNumber: str, offset: int = 0):
        cache_key = f"stock_{stockNumber}_{offset}"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                trade_date as time, 
                                open_price as open, 
                                high_price as high, 
                                low_price as low, 
                                close_price as close, 
                                trade_volume as value,
                                name,
                                stock_prices.number
                            FROM stock_prices 
                            JOIN stock_name ON stock_prices.number = stock_name.number 
                            WHERE stock_prices.number = %s 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [stockNumber,offset])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TAIEX_KLine(offset: int = 0):
        cache_key = f"index_TAIEX_{offset}"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                trade_date as time, 
                                open_price as open, 
                                high_price as high, 
                                low_price as low, 
                                close_price as close, 
                                trade_value as value 
                            FROM TAIEX_prices 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [offset])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TPEX_KLine(offset: int = 0):
        cache_key = f"index_TPEX_{offset}"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                trade_date as time, 
                                open_price as open, 
                                high_price as high, 
                                low_price as low, 
                                close_price as close, 
                                trade_value as value 
                            FROM TPEX_prices 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [offset])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    