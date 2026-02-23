from services.twse_stock_service import TwseStock
from services.twse_index_service import TwseIndex
from models.stock_model import StockModel
from utils.data_utils import FormatHelper
import time, random
from datetime import timedelta, date

def get_TwseStock_data(start_date, end_date):  # 資料進度 2023, 1, 1
    number_data = set(StockModel.get_all_stock_numbers())
    while start_date >= end_date:
        if start_date.weekday() >= 5:
            start_date -= timedelta(days=1)
            continue
        url=TwseStock.get_TWstock_url(start_date)
        jsondata=TwseStock.get_TWstock_json(url)
        stock_data=TwseStock.clean_jsondata(jsondata, number_data, start_date)
        if stock_data:          
            StockModel.save_stock_prices(stock_data)
            print(f"[{start_date}] 儲存完成。")
        else:
            print(f"[{start_date}] 無資料 (可能是休市)。")

        start_date -= timedelta(days=1)
        sleep_time = random.uniform(5, 12) 
        time.sleep(sleep_time)

start = date(2022, 7, 1)
end = date(2022, 6, 1)
get_TwseStock_data(start, end)

# def get_TwseIndex_data(start_date, end_date):