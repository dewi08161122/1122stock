from services.twse_stock_service import TwseStock
from models.stock_model import StockModel
from utils.data_utils import FormatHelper
import time, random
from datetime import timedelta, date

def get_TwseStock_data(start_date, end_date):
    number_data = set(StockModel.get_all_stock_numbers())
    while start_date >= end_date:
        if start_date.weekday() >= 5:
            start_date -= timedelta(days=1)
            continue
        url=TwseStock.get_TWstock_url(start_date)
        jsondata=TwseStock.get_TWstock_json(url)
        stock_data=TwseStock.clean_jsondata(jsondata)
        if stock_data:
            day_records = []
            for i in stock_data:
                if i[0] in number_data:
                    change_price = FormatHelper.clean_value_to_float(i[10])
                    if "-" in i[9] or "green" in i[9]:
                        change_price = -abs(change_price)
                    record = (
                        i[0], 
                        start_date.strftime("%Y-%m-%d"), 
                        FormatHelper.clean_value_to_float(i[5]),
                        FormatHelper.clean_value_to_float(i[8]),
                        FormatHelper.clean_value_to_float(i[6]),
                        FormatHelper.clean_value_to_float(i[7]),
                        change_price,
                        FormatHelper.clean_value_to_int(i[2]),
                        FormatHelper.clean_value_to_int(i[4])
                    )
                    day_records.append(record)
            
            StockModel.save_stock_prices(day_records)
            print(f"[{start_date}] 儲存完成。")
        else:
            print(f"[{start_date}] 無資料 (可能是休市)。")

        start_date -= timedelta(days=1)
        sleep_time = random.uniform(5, 12) 
        time.sleep(sleep_time)

# start = date(2026, 2, 1)
# end = date(2026, 1, 1)
# get_TwseStock_data(start, end)