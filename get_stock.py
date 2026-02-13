import urllib.request as req
import json


def get_stock_url(stock_no, date_str):
    base_url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
    url = f"{base_url}?date={date_str}&stockNo={stock_no}&response=json"
    return url

target_url = get_stock_url("2330", "20240201")

def get_stock_data(target_url):
    request = req.Request(target_url, headers={
        "User-Agent": "Mozilla/5.0"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    result = json.loads(data)
    print(result["data"])

get_stock_data(target_url)