from infrastructure.connection import get_connection
import json, requests
from bs4 import BeautifulSoup

try:
    with open("data/TW_company_data.json", "r", encoding="utf-8") as file:
        TWdata=json.load(file)
    with open("data/TWO_company_data.json", "r", encoding="utf-8") as file:
        TWOdata=json.load(file)
    url = "https://isin.twse.com.tw/isin/class_i.jsp?kind=1"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    with get_connection() as con:
        with con.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS stock_name(" \
            "id BIGINT unsigned NOT NULL primary key auto_increment," \
            "number VARCHAR(255) NOT NULL," \
            "name VARCHAR(255) NOT NULL," \
            "category VARCHAR(255) NOT NULL," \
            "market_type VARCHAR(255) NOT NULL)"
            )
            # cursor.execute("CREATE TABLE IF NOT EXISTS stock_prices(" \
			# "id BIGINT unsigned not null primary key auto_increment," \
			# "number VARCHAR(255) not null," \
			# "name VARCHAR(255) not null," \
			# "category VARCHAR(255) not null)"
			# )

            for i in TWdata:
                number = i.get("公司代號")
                name = i.get("公司簡稱")
                category = i.get("產業別")
                
                if number and name and category:
                    cursor.execute(
                        "INSERT INTO stock_name(number, name, category, market_type) VALUES(%s, %s, %s, %s)",
                        (number, name, category, "上市")
                    )
                else:
                    print(f"不完整的資料: {i}")

            for i in TWOdata:
                number = i.get("SecuritiesCompanyCode")
                name = i.get("CompanyAbbreviation")
                category = i.get("SecuritiesIndustryCode")
                
                if number and name and category:
                    cursor.execute(
                        "INSERT INTO stock_name(number, name, category, market_type) VALUES(%s, %s, %s, %s)",
                        (number, name, category,"上櫃")
                    )
                else:
                    print(f"不完整的資料: {i}")
            con.commit()

except Exception as e:
    print(f"初始化資料庫失敗: {e}")

