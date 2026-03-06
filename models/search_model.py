from infrastructure.connection import get_connection

class SearchModel:
    @staticmethod
    def get_category():
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT category_name FROM stock_category ORDER BY category_number ASC")
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_categorystock(category_name: str):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT number, name FROM stock_name JOIN stock_category ON stock_name.category_number = stock_category.category_number WHERE category_name = %s ORDER BY number ASC",[category_name])
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)
    @staticmethod
    def get_trade_value_ranking(category_name: str):
        try:
            with get_connection() as con:
                with con.cursor(dictionary=True) as cursor:
                    cursor.execute("SELECT trade_date as time, open_price as open, high_price as high, low_price as low, close_price as close, change_price as change_price,(change_price / (close_price - change_price) * 100) as percent FROM stock_price JOIN stock_name ON stock_price.number = stock_name.number WHERE trade_date = %s ORDER BY trade_value DESC LIMIT 30",[category_name])
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            print(e)