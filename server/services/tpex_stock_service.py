from utils.data_utils import FormatHelper
import requests

class TpexStock:
    @staticmethod
    def get_Tpexstock_data(date):
        url = "https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes" 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        date_str = date.strftime("%Y/%m/%d")
        payload = {
            "date": date_str,
            "id": "",
            "response": "json"
        }
        session = requests.Session()
        response = session.post(url, data=payload, headers=headers, verify=False)
        data = response.json()

        return data
    @staticmethod
    def clean_Tpexstock_data(jsondata, number_data, start_date):
        stock_data = jsondata['tables'][0].get('data', [])
        if stock_data:
            day_records = []
            date_str = start_date.strftime("%Y-%m-%d")
            for i in stock_data:
                if i[0] in number_data:              
                    record = (
                        i[0], 
                        date_str, 
                        FormatHelper.clean_value_to_float(i[4]),
                        FormatHelper.clean_value_to_float(i[2]),
                        FormatHelper.clean_value_to_float(i[5]),
                        FormatHelper.clean_value_to_float(i[6]),
                        FormatHelper.clean_value_to_float(i[3]),
                        FormatHelper.clean_value_to_int(i[8]),
                        FormatHelper.clean_value_to_int(i[9])
                    )
                    day_records.append(record)
            return day_records
        return None