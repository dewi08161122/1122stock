from infrastructure.connection import get_connection

class FunctionModel:
    @staticmethod
    def increase_observe(user_id, number):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("INSERT IGNORE INTO member_observe_stock(id,number) VALUES(%s,%s)",[user_id, number])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def delete_observe(user_id, number):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("DELETE FROM member_observe_stock WHERE id = %s AND number = %s",[user_id, number])
                    con.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_observe(user_id, trade_date: str):
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
                        WHERE p.trade_date = %s AND m.id = %s
                        ORDER BY m.number ASC
                    """
                    cursor.execute(sql, [trade_date, user_id])
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