from infrastructure.connection import get_connection

class KLineModel:
    @staticmethod
    def get_stock_KLine(stockNumber: str):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, trade_volume as value FROM stock_prices WHERE number=%s ORDER BY trade_date ASC",[stockNumber])
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"])
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_TAIEX_KLine():
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, trade_value as value FROM TAIEX_prices ORDER BY trade_date ASC")
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"])
                    print(result)
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_TPEX_KLine():
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, trade_value as value FROM TPEX_prices ORDER BY trade_date ASC")
                    result = cursor.fetchall()
                    for i in result:
                        i["time"]=str(i["time"])
                        i["open"]=float(i["open"])
                        i["high"]=float(i["high"])
                        i["low"]=float(i["low"])
                        i["close"]=float(i["close"])
                        i["value"]=int(i["value"])
                    return result
        except Exception as e:
            print(e)
