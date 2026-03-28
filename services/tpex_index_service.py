from utils.data_utils import FormatHelper
import requests, re

class TpexIndex:
    @staticmethod
    def get_TpexIndex_data(date):
        url = "https://www.tpex.org.tw/www/zh-tw/indexInfo/inx" 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.tpex.org.tw/zh-tw/mainboard/after-trading/daily-close-quotes.html',
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
    def clean_TpexIndex_data_without_value(jsondata):
        index_data = jsondata['tables'][0].get('data', [])
        if index_data:
            records = []
            for i in index_data:
                record = (
                    i[0].replace('/', '-'),
                    FormatHelper.clean_value_to_float(i[1]),
                    FormatHelper.clean_value_to_float(i[4]),
                    FormatHelper.clean_value_to_float(i[2]),
                    FormatHelper.clean_value_to_float(i[3]),
                    FormatHelper.clean_value_to_float(i[5]),
                )
                records.append(record)
            return records
        return None
    
    @staticmethod
    def clean_TpexIndex_valuedata(jsondata):
        subtitle = jsondata['tables'][0].get('subtitle', '') 
        match = re.search(r"總成交金額:\s*([\d,]+)", subtitle)
        if match:
            value = FormatHelper.clean_value_to_int(match.group(1))
            return value