from infrastructure.connection import get_connection

class StockModel:
    @staticmethod
    def save_stock_category(cursor, number, name):
        cursor.execute(
            "INSERT INTO stock_category(category_number, category_name) VALUES(%s, %s) ON DUPLICATE KEY UPDATE category_name = VALUES(category_name)",(number, name)
        )
    @staticmethod
    def save_stock_name(cursor, number, name, category, market_type):
        cursor.execute(
            "INSERT INTO stock_name(number, name, category_number, market_type) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name), category_number = VALUES(category_number), market_type = VALUES(market_type)",(number, name, category, market_type)
        )
    @staticmethod
    def save_stock_prices(stock_prices_list):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.executemany(
                        "INSERT IGNORE INTO stock_prices(number, trade_date, open_price, close_price, high_price, low_price, change_price, trade_volume, trade_value) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",stock_prices_list
                    )
                    con.commit()
        except Exception as e:
            print(f"批次儲存失敗: {e}")
    @staticmethod
    def save_TAIEX_prices(TAIEX_prices_list):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.executemany(
                        "INSERT IGNORE INTO TAIEX_prices(trade_date, open_price, close_price, high_price, low_price, change_price, trade_value) VALUES(%s, %s, %s, %s, %s, %s, %s)",TAIEX_prices_list
                    )
                    con.commit()
        except Exception as e:
            print(f"批次儲存失敗: {e}")
    @staticmethod
    def get_all_stock_numbers():
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute("SELECT number FROM stock_name")
                    return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"資料庫讀取失敗: {e}")
            return []