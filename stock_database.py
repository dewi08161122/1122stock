from infrastructure.connection import get_connection
import json

try:
    with open("data/TW_company_data.json", "r", encoding="utf-8") as file:
        TWdata=json.load(file)
    with open("data/TWO_company_data.json", "r", encoding="utf-8") as file:
        TWOdata=json.load(file)

    with get_connection() as con:
		with con.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS stock_name(" \
			"id BIGINT unsigned not null primary key auto_increment," \
			"number varchar(255) not null," \
			"name varchar(255) not null," \
			"category varchar(255) not null)";
			)
        with con.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS stock_prices(" \
			"id BIGINT unsigned not null primary key auto_increment," \
			"number varchar(255) not null," \
			"name varchar(255) not null," \
			"category varchar(255) not null)";
			)

        for i in TWdata:
            number=i["公司代號"]
            name=i["公司簡稱"]
            category=["產業別"]
            cursor.execute("INSERT INTO stock_name(nember,name,category) VALUES(%s,%s,%s)",[number,name,category])
            con.commit()
        
        for i in TWOdata:
            number=i["公司代號"]
            name=i["公司簡稱"]
            category=["產業別"]
            cursor.execute("INSERT INTO stock_name(nember,name,category) VALUES(%s,%s,%s)",[number,name,category])
            con.commit()

except Exception as e:
    print(f"初始化資料庫失敗: {e}")

