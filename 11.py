import requests, pandas
from infrastructure.connection import get_connection

url = "https://isin.twse.com.tw/isin/class_i.jsp?kind=1"
response = requests.get(url, verify=False)

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
                cursor.execute("INSERT INTO stock_category(category_number, category_name) VALUES(%s, %s,)",(number, name))