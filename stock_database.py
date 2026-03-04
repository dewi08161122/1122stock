from models.save_stock_model import StockModel
from infrastructure.connection import get_connection
import json, requests, pandas

category_url = "https://isin.twse.com.tw/isin/class_i.jsp?kind=1"

try:
    with open("data/TW_company_data.json", "r", encoding="utf-8") as file:
        TWdata=json.load(file)
    with open("data/TWO_company_data.json", "r", encoding="utf-8") as file:
        TWOdata=json.load(file)

    response = requests.get(category_url, verify=False)
    data = pandas.read_html(response.content, encoding='utf-8')
    list=data[0].iloc[5, 1]
    items = list.split(' ')
    
    with get_connection() as con:
        with con.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS stock_category(" \
            "id BIGINT unsigned not null primary key auto_increment," \
            "category_number varchar(255) not null," \
            "category_name varchar(255) not null," \
            "UNIQUE KEY (category_number));"
			)
            for i in items:
                if '.' in i:
                    category=i.split('.')
                    number = category[0]
                    name = category[1]
                    StockModel.save_stock_category(cursor, number, name)
            StockModel.save_stock_category(cursor, "91", "存託憑證")

            cursor.execute("CREATE TABLE IF NOT EXISTS stock_name(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "number VARCHAR(20) NOT NULL," \
            "name VARCHAR(100) NOT NULL," \
            "category_number VARCHAR(100) NOT NULL," \
            "market_type VARCHAR(20) NOT NULL," \
            "FOREIGN KEY (category_number) REFERENCES stock_category (category_number) ON UPDATE CASCADE," \
            "UNIQUE KEY (number)," \
            "INDEX (name))"
            )

            for i in TWdata:
                number = i.get("公司代號")
                name = i.get("公司簡稱")
                category = i.get("產業別")
                
                if number and name and category:
                    StockModel.save_stock_name(cursor, number, name, category, "上市")
                else:
                    print(f"不完整的資料: {i}")

            for i in TWOdata:
                number = i.get("SecuritiesCompanyCode")
                name = i.get("CompanyAbbreviation")
                category = i.get("SecuritiesIndustryCode")
                
                if number and name and category:
                    StockModel.save_stock_name(cursor, number, name, category, "上櫃")
                else:
                    print(f"不完整的資料: {i}")
            cursor.execute("CREATE TABLE IF NOT EXISTS stock_prices(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "number VARCHAR(20) NOT NULL," \
            "trade_date DATE NOT NULL," \
            "open_price DECIMAL(10, 2)," \
            "close_price DECIMAL(10, 2)," \
            "high_price DECIMAL(10, 2)," \
            "low_price DECIMAL(10, 2)," \
            "change_price DECIMAL(10, 2)," \
            "trade_volume BIGINT," \
            "trade_value BIGINT," \
            "FOREIGN KEY (number) REFERENCES stock_name (number) ON UPDATE CASCADE," \
            "UNIQUE KEY (number, trade_date)," \
            "INDEX (trade_date))"
            )
            cursor.execute("CREATE TABLE IF NOT EXISTS TAIEX_prices(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "trade_date DATE NOT NULL," \
            "open_price DECIMAL(10, 2)," \
            "close_price DECIMAL(10, 2)," \
            "high_price DECIMAL(10, 2)," \
            "low_price DECIMAL(10, 2)," \
            "change_price DECIMAL(10, 2)," \
            "trade_value BIGINT," \
            "UNIQUE KEY (trade_date))"
            )
            cursor.execute("CREATE TABLE IF NOT EXISTS TPEX_prices(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "trade_date DATE NOT NULL," \
            "open_price DECIMAL(10, 2)," \
            "close_price DECIMAL(10, 2)," \
            "high_price DECIMAL(10, 2)," \
            "low_price DECIMAL(10, 2)," \
            "change_price DECIMAL(10, 2)," \
            "trade_value BIGINT," \
            "UNIQUE KEY (trade_date))"
            )
            cursor.execute("CREATE TABLE IF NOT EXISTS member(" \
			"id BIGINT unsigned not null primary key auto_increment," \
			"email varchar(255) not null," \
			"password varchar(255) not null);"
			)
            cursor.execute("CREATE TABLE IF NOT EXISTS member_stock(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "user_id BIGINT unsigned not null," \
            "number VARCHAR(20) NOT NULL," \
            "user_type VARCHAR(20) NOT NULL," \
            "FOREIGN KEY (user_id) REFERENCES member (id)," \
            "FOREIGN KEY (number) REFERENCES stock_name (number) ON UPDATE CASCADE)"
            )
            con.commit()

except Exception as e:
    print(f"初始化資料庫失敗: {e}")
