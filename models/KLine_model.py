from infrastructure.connection import get_connection

class KLineModel:
    @staticmethod
    def get_stock_KLine(stockNumber: str, offset: int = 0):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                DATE_FORMAT(trade_date, '%Y-%m-%d') as time, 
                                CAST(open_price AS FLOAT) as open, 
                                CAST(high_price AS FLOAT) as high, 
                                CAST(low_price AS FLOAT) as low, 
                                CAST(close_price AS FLOAT) as close, 
                                CAST(trade_volume AS UNSIGNED) as value,
                                name, 
                                stock_prices.number as number 
                            FROM stock_prices 
                            JOIN stock_name ON 
                            stock_prices.number = stock_name.number 
                            WHERE stock_prices.number = %s 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [stockNumber, offset])
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_TAIEX_KLine(offset: int = 0):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                DATE_FORMAT(trade_date, '%Y-%m-%d') as time, 
                                CAST(open_price AS FLOAT) as open, 
                                CAST(high_price AS FLOAT) as high, 
                                CAST(low_price AS FLOAT) as low, 
                                CAST(close_price AS FLOAT) as close, 
                                CAST(IFNULL(trade_value, 0) AS UNSIGNED) as value 
                            FROM TAIEX_prices 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [offset])
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_TPEX_KLine(offset: int = 0):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT * FROM (
                            SELECT 
                                DATE_FORMAT(trade_date, '%Y-%m-%d') as time, 
                                CAST(open_price AS FLOAT) as open, 
                                CAST(high_price AS FLOAT) as high, 
                                CAST(low_price AS FLOAT) as low, 
                                CAST(close_price AS FLOAT) as close, 
                                CAST(IFNULL(trade_value, 0) AS UNSIGNED) as value 
                            FROM TPEX_prices 
                            ORDER BY trade_date DESC 
                            LIMIT 500 OFFSET %s
                        ) AS subquery
                        ORDER BY time ASC
                    """
                    cursor.execute(sql, [offset])
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
    