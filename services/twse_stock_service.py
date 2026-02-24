from utils.data_utils import FormatHelper

class TwseStock:
    @staticmethod
    def get_TWstock_url(date):
        date_str = date.strftime("%Y%m%d")
        url = f"https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={date_str}&type=ALLBUT0999&response=json"
        return url
    
    @staticmethod
    def clean_stock_data(jsondata, number_data, start_date):
        stock_data = None
        for table in jsondata.get("tables", []):
            if "每日收盤行情" in table.get('title', ''):
                stock_data = table.get('data', [])
                break
        if stock_data:
            day_records = []
            date_str = start_date.strftime("%Y-%m-%d")
            for i in stock_data:
                if i[0] in number_data:
                    change_price = FormatHelper.clean_value_to_float(i[10])
                    if "-" in i[9] or "green" in i[9]:
                        change_price = -abs(change_price)
                    record = (
                        i[0], 
                        date_str, 
                        FormatHelper.clean_value_to_float(i[5]),
                        FormatHelper.clean_value_to_float(i[8]),
                        FormatHelper.clean_value_to_float(i[6]),
                        FormatHelper.clean_value_to_float(i[7]),
                        change_price,
                        FormatHelper.clean_value_to_int(i[2]),
                        FormatHelper.clean_value_to_int(i[4])
                    )
                    day_records.append(record)
            return day_records
        return None
    