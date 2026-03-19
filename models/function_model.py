from infrastructure.connection import get_connection

class FunctionModel:
    @staticmethod
    def increase_observe(user_id: int, number: str):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("INSERT IGNORE INTO member_observe_stock(user_id,number) VALUES(%s,%s)",[user_id, number])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def delete_observe(user_id: int, number: str):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("DELETE FROM member_observe_stock WHERE user_id = %s AND number = %s",[user_id, number])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_observe(user_id: int):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT p.trade_date as time,
                        p.open_price as open,
                        p.high_price as high,
                        p.low_price as low,
                        p.close_price as close,
                        p.change_price as change_price,
                        (p.change_price / (p.close_price - p.change_price) * 100) as percent,
                        m.number,
                        n.name 
                        FROM member_observe_stock AS m 
                        JOIN stock_name AS n ON m.number = n.number 
                        JOIN stock_prices AS p ON m.number = p.number
                        WHERE m.user_id = %s AND p.trade_date = (SELECT MAX(trade_date) FROM stock_prices) 
                        ORDER BY m.number ASC
                    """
                    cursor.execute(sql, (user_id,))
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["change_price"]=float(i["change_price"])
                        i["percent"]=float(i["percent"])
                    return result
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def increase_hold(user_id: int, number: str, hold_volume: int, hold_price: float, trade_date: str):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("INSERT INTO member_stock_transactions(user_id, number, hold_volume, hold_price, trade_date) VALUES(%s,%s,%s,%s,%s)",[user_id, number, hold_volume, hold_price, trade_date])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def put_hold(id: int, user_id: int, hold_volume: int, hold_price: float, trade_date: str):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("UPDATE member_stock_transactions SET hold_volume = %s, hold_price = %s, trade_date = %s WHERE id = %s AND user_id = %s",[hold_volume, hold_price, trade_date, id, user_id])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def delete_hold_by_number(user_id: int, number: str):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("DELETE FROM member_stock_transactions WHERE user_id = %s AND number = %s",[user_id, number])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def delete_hold_by_id(user_id: int, id: int):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("DELETE FROM member_stock_transactions WHERE id = %s AND user_id = %s",[id, user_id])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_hold(user_id: int):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT m.number,
                        n.name,
                        SUM(m.hold_volume) as total_volume,
                        ((MAX(p.close_price) * SUM(m.hold_volume)) - SUM(m.hold_price * m.hold_volume)) as pnl,
                        COALESCE(((MAX(p.close_price) * SUM(m.hold_volume)) - SUM(m.hold_price * m.hold_volume)) / NULLIF(SUM(m.hold_price * m.hold_volume), 0) * 100 , 0) as roi,
                        ROUND(SUM(m.hold_price * m.hold_volume) / SUM(m.hold_volume), 2) AS avg_cos,
                        SUM(m.hold_price * m.hold_volume) as cost,
                        MAX(p.close_price) as close,
                        (MAX(p.close_price) * SUM(m.hold_volume)) as value 
                        FROM member_stock_transactions AS m 
                        JOIN stock_name AS n ON m.number = n.number 
                        JOIN stock_prices AS p ON m.number = p.number
                        WHERE m.user_id = %s AND p.trade_date = (SELECT MAX(trade_date) FROM stock_prices) 
                        GROUP BY m.number, n.name
                        ORDER BY m.number ASC
                    """
                    cursor.execute(sql, (user_id,))
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def get_hold_by_number(user_id: int, number: str):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT m.id, 
                        m.number,
                        n.name,
                        m.hold_volume as hold_volume,
                        m.hold_price as hold_price,
                        m.trade_date as trade_date 
                        FROM member_stock_transactions AS m 
                        JOIN stock_name AS n ON m.number = n.number 
                        WHERE m.user_id = %s AND m.number = %s 
                        ORDER BY m.id ASC
                    """
                    cursor.execute(sql, (user_id, number))
                    result = cursor.fetchall()
                    for i in result:
                        i["trade_date"]=str(i["trade_date"])
                    return result
        except Exception as e:
            print(e)
            return [] 