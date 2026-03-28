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
                            SELECT * FROM (
                                SELECT 
                                    trade_date as time, 
                                    open_price as open, 
                                    high_price as high, 
                                    low_price as low, 
                                    close_price as close, 
                                    trade_volume as value,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60,
                                    name,
                                    stock_prices.number
                                FROM stock_prices 
                                JOIN stock_name ON stock_prices.number = stock_name.number 
                                WHERE stock_prices.number = %s 
                                ORDER BY time DESC 
                                LIMIT 560 OFFSET %s
                            ) AS full_data 
                            LIMIT 500
                        ) AS page_data
                        ORDER BY time ASC
                    """# BETWEEN ... AND ...定義範圍,PRECEDING往前數幾筆,CURRENT ROW=包含現在這一筆
                    cursor.execute(sql, [stockNumber,offset])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_stock_KLine_week(stockNumber: str):
        cache_key = f"stock_{stockNumber}_week"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_volume as value,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60,
                            name,
                            stock_prices_week.number
                        FROM stock_prices_week 
                        JOIN stock_name ON stock_prices_week.number = stock_name.number 
                        WHERE stock_prices_week.number = %s 
                        ORDER BY time ASC 
                    """
                    cursor.execute(sql, [stockNumber])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_stock_KLine_month(stockNumber: str):
        cache_key = f"stock_{stockNumber}_month"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_volume as value,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60,
                            name,
                            stock_prices_month.number
                        FROM stock_prices_month 
                        JOIN stock_name ON stock_prices_month.number = stock_name.number 
                        WHERE stock_prices_month.number = %s 
                        ORDER BY time ASC 
                    """
                    cursor.execute(sql, [stockNumber])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
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
                            SELECT * FROM (
                                SELECT 
                                    trade_date as time, 
                                    open_price as open, 
                                    high_price as high, 
                                    low_price as low, 
                                    close_price as close, 
                                    trade_value as value, 
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                                FROM TAIEX_prices 
                                ORDER BY trade_date DESC 
                                LIMIT 560 OFFSET %s
                            ) AS full_data 
                            LIMIT 500
                        ) AS page_data
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
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TAIEX_KLine_week():
        cache_key = f"index_TAIEX_week"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_value as value, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                        FROM TAIEX_prices_week 
                        ORDER BY first_trade_date ASC
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TAIEX_KLine_month():
        cache_key = f"index_TAIEX_month"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_value as value, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                        FROM TAIEX_prices_month 
                        ORDER BY first_trade_date ASC
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
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
                            SELECT * FROM (
                                SELECT 
                                    trade_date as time, 
                                    open_price as open, 
                                    high_price as high, 
                                    low_price as low, 
                                    close_price as close, 
                                    trade_value as value, 
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                                    AVG(close_price) OVER(ORDER BY trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                                FROM TPEX_prices 
                                ORDER BY trade_date DESC 
                                LIMIT 560 OFFSET %s
                            ) AS full_data 
                            LIMIT 500
                        ) AS page_data
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
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TPEX_KLine_week():
        cache_key = f"index_TPEX_week"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_value as value, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                        FROM TPEX_prices_week 
                        ORDER BY first_trade_date ASC
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def get_TPEX_KLine_month():
        cache_key = f"index_TPEX_month"
        if cache_key in KLINE_CACHE:
            return KLINE_CACHE[cache_key]
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT 
                            first_trade_date as time, 
                            first_open_price as open, 
                            max_high_price as high, 
                            min_low_price as low, 
                            last_close_price as close, 
                            total_trade_value as value, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) as ma5, 
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) as ma10,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as ma20,
                            AVG(last_close_price) OVER(ORDER BY first_trade_date ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) as ma60
                        FROM TPEX_prices_month 
                        ORDER BY first_trade_date ASC
                    """
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"]) if i["value"] is not None else 0
                        i["ma5"] = float(i["ma5"]) if i["ma5"] is not None else 0
                        i["ma10"] = float(i["ma10"]) if i["ma10"] is not None else 0
                        i["ma20"] = float(i["ma20"]) if i["ma20"] is not None else 0
                        i["ma60"] = float(i["ma60"]) if i["ma60"] is not None else 0
                    if result:
                        KLINE_CACHE[cache_key] = result
                    return result
        except Exception as e:
            print(e)
            return None