import requests, time, random, pandas
from datetime import date, timedelta


class TwseStock:
    @staticmethod
    def get_TWstock_url(date):
        date_str = date.strftime("%Y%m%d")
        url = f"https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={date_str}&type=ALLBUT0999&response=json"
        return url
    
    @staticmethod
    def get_TWstock_json(TWstock_url):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.twse.com.tw/"
        }
        response = requests.get(TWstock_url, headers=headers, verify=False)
        if response.status_code != 200:
            print("請求失敗")
            return None
        data = response.json()
        return data
    
    @staticmethod
    def clean_jsondata(jsondata):

        for table in jsondata.get("tables", []):
            if "每日收盤行情" in table.get('title', ''):
                stock_data = table.get('data', [])
                return stock_data
        return None
    