from infrastructure.connection import get_connection

class StockModel:
    @staticmethod
    def save_stock_category(cursor, number, name):
        cursor.execute(
            "INSERT INTO stock_category(category_number, category_name) VALUES(%s, %s) ON DUPLICATE KEY UPDATE category_number = VALUES(category_number), category_name = VALUES(category_name)",(number, name)
        )
    @staticmethod
    def save_stock_name(cursor, number, name, category, market_type):
        cursor.execute(
            "INSERT INTO stock_name(number, name, category_number, market_type) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name), category_number = VALUES(category_number), market_type = VALUES(market_type)",(number, name, category, market_type)
        )