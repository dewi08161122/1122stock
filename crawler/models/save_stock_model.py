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
                    sql = """
                        INSERT INTO stock_prices (
                            number, trade_date, open_price, close_price, 
                            high_price, low_price, change_price, trade_volume, trade_value
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            open_price = VALUES(open_price),
                            close_price = VALUES(close_price),
                            high_price = VALUES(high_price),
                            low_price = VALUES(low_price),
                            change_price = VALUES(change_price),
                            trade_volume = VALUES(trade_volume),
                            trade_value = VALUES(trade_value)
                    """
                    cursor.executemany(sql, stock_prices_list)
                    con.commit()
        except Exception as e:
            print(f"批次儲存失敗: {e}")
    @staticmethod
    def save_TAIEX_prices(TAIEX_prices_list):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    sql = """
                        INSERT INTO TAIEX_prices (
                            trade_date, open_price, close_price, 
                            high_price, low_price, change_price, trade_value
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            open_price = VALUES(open_price),
                            close_price = VALUES(close_price),
                            high_price = VALUES(high_price),
                            low_price = VALUES(low_price),
                            change_price = VALUES(change_price),
                            trade_value = VALUES(trade_value)
                    """
                    cursor.executemany(sql, TAIEX_prices_list)
                    con.commit()
        except Exception as e:
            print(f"批次儲存失敗: {e}")
    @staticmethod
    def save_TPEX_prices(TPEX_prices_list):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    sql = """
                        INSERT INTO TPEX_prices (
                            trade_date, open_price, close_price, 
                            high_price, low_price, change_price
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            open_price = VALUES(open_price),
                            close_price = VALUES(close_price),
                            high_price = VALUES(high_price),
                            low_price = VALUES(low_price),
                            change_price = VALUES(change_price)
                    """
                    cursor.executemany(sql, TPEX_prices_list)
                    con.commit()
        except Exception as e:
            print(f"批次儲存失敗: {e}")
    @staticmethod
    def save_TPEX_value(value, date):
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    cursor.execute(
                        "UPDATE TPEX_prices SET trade_value = %s WHERE trade_date = %s",(value, date)
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
    @staticmethod
    def all_kline_to_week_month(target_date):  
        try:
            with get_connection() as con:
                with con.cursor() as cursor:
                    stock_week_sql = """
                        INSERT INTO stock_prices_week (number, first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_volume, total_trade_value)
                        SELECT d1.number, MIN(d1.trade_date),
                            (SELECT open_price FROM stock_prices d2 WHERE d2.number = d1.number AND d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM stock_prices d3 WHERE d3.number = d1.number AND d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(d1.high_price), MIN(d1.low_price), SUM(d1.trade_volume), SUM(d1.trade_value)
                        FROM stock_prices d1
                        WHERE d1.number IN (SELECT number FROM stock_prices WHERE trade_date = %s)
                          AND YEARWEEK(d1.trade_date, 1) = YEARWEEK(%s, 1)
                        GROUP BY d1.number, YEARWEEK(d1.trade_date, 1)
                        ON DUPLICATE KEY UPDATE 
                            last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price),
                            min_low_price = VALUES(min_low_price), total_trade_volume = VALUES(total_trade_volume), total_trade_value = VALUES(total_trade_value);
                    """
                    stock_month_sql = """
                        INSERT INTO stock_prices_month (number, first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_volume, total_trade_value)
                        SELECT d1.number, MIN(d1.trade_date),
                            (SELECT open_price FROM stock_prices d2 WHERE d2.number = d1.number AND d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM stock_prices d3 WHERE d3.number = d1.number AND d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(d1.high_price), MIN(d1.low_price), SUM(d1.trade_volume), SUM(d1.trade_value)
                        FROM stock_prices d1
                        WHERE d1.number IN (SELECT number FROM stock_prices WHERE trade_date = %s)
                          AND DATE_FORMAT(d1.trade_date, '%Y-%m') = DATE_FORMAT(%s, '%Y-%m')
                        GROUP BY d1.number, DATE_FORMAT(d1.trade_date, '%Y-%m')
                        ON DUPLICATE KEY UPDATE 
                            last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price),
                            min_low_price = VALUES(min_low_price), total_trade_volume = VALUES(total_trade_volume), total_trade_value = VALUES(total_trade_value);
                    """
                    TAIEX_week_sql = """
                        INSERT INTO TAIEX_prices_week (first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_value)
                        SELECT MIN(trade_date),
                            (SELECT open_price FROM TAIEX_prices d2 WHERE d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM TAIEX_prices d3 WHERE d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(high_price), MIN(low_price), SUM(trade_value)
                        FROM TAIEX_prices d1 WHERE YEARWEEK(trade_date, 1) = YEARWEEK(%s, 1)
                        ON DUPLICATE KEY UPDATE last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price), min_low_price = VALUES(min_low_price), total_trade_value = VALUES(total_trade_value);
                    """
                    TAIEX_month_sql = """
                        INSERT INTO TAIEX_prices_month (first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_value)
                        SELECT MIN(trade_date),
                            (SELECT open_price FROM TAIEX_prices d2 WHERE d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM TAIEX_prices d3 WHERE d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(high_price), MIN(low_price), SUM(trade_value)
                        FROM TAIEX_prices d1 WHERE DATE_FORMAT(trade_date, '%Y-%m') = DATE_FORMAT(%s, '%Y-%m')
                        ON DUPLICATE KEY UPDATE last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price), min_low_price = VALUES(min_low_price), total_trade_value = VALUES(total_trade_value);
                    """
                    TPEX_week_sql = """
                        INSERT INTO TPEX_prices_week (first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_value)
                        SELECT MIN(trade_date),
                            (SELECT open_price FROM TPEX_prices d2 WHERE d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM TPEX_prices d3 WHERE d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(high_price), MIN(low_price), SUM(trade_value)
                        FROM TPEX_prices d1 WHERE YEARWEEK(trade_date, 1) = YEARWEEK(%s, 1)
                        ON DUPLICATE KEY UPDATE last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price), min_low_price = VALUES(min_low_price), total_trade_value = VALUES(total_trade_value);
                    """
                    TPEX_month_sql = """
                        INSERT INTO TPEX_prices_month (first_trade_date, first_open_price, last_close_price, max_high_price, min_low_price, total_trade_value)
                        SELECT MIN(trade_date),
                            (SELECT open_price FROM TPEX_prices d2 WHERE d2.trade_date = MIN(d1.trade_date) LIMIT 1),
                            (SELECT close_price FROM TPEX_prices d3 WHERE d3.trade_date = MAX(d1.trade_date) LIMIT 1),
                            MAX(high_price), MIN(low_price), SUM(trade_value)
                        FROM TPEX_prices d1 WHERE DATE_FORMAT(trade_date, '%Y-%m') = DATE_FORMAT(%s, '%Y-%m')
                        ON DUPLICATE KEY UPDATE last_close_price = VALUES(last_close_price), max_high_price = VALUES(max_high_price), min_low_price = VALUES(min_low_price), total_trade_value = VALUES(total_trade_value);
                    """

                    cursor.execute(stock_week_sql, [target_date, target_date])
                    cursor.execute(stock_month_sql, [target_date, target_date])
                    cursor.execute(TAIEX_week_sql, [target_date])
                    cursor.execute(TAIEX_month_sql, [target_date])
                    cursor.execute(TPEX_week_sql, [target_date])
                    cursor.execute(TPEX_month_sql, [target_date])
                                     
                    con.commit()
                    print(f"[{target_date}] 週/月K更新完成。")
        except Exception as e:
            print(f"同步過程出錯: {e}")