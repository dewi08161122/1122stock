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