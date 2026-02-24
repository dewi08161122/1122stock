from services.twse_stock_service import TwseStock
from services.twse_index_service import TwseIndex
from services.tpex_stock_service import TpexStock
from models.stock_model import StockModel
from infrastructure.network import get_json_by_url
import time, random
from datetime import timedelta, date

def get_TwseStock_data(start_date, end_date):  # 資料進度 2019, 7, 1
    number_data = set(StockModel.get_all_stock_numbers())
    while start_date >= end_date:
        if start_date.weekday() >= 5:
            start_date -= timedelta(days=1)
            continue
        url=TwseStock.get_TWstock_url(start_date)
        jsondata=get_json_by_url(url)
        stock_data=TwseStock.clean_TWstock_data(jsondata, number_data, start_date)
        if stock_data:          
            StockModel.save_stock_prices(stock_data)
            print(f"[{start_date}] 儲存完成。")
        else:
            print(f"[{start_date}] 無資料 (可能是休市)。")

        start_date -= timedelta(days=1)
        sleep_time = random.uniform(5, 12) 
        time.sleep(sleep_time)

# start = date(2019, 7, 1)
# end = date(2019, 1, 1)
# get_TwseStock_data(start, end) # 上市個股進度

def get_TwseIndex_data(start_date, end_date):  # 資料進度 2020, 1, 1
    while start_date >= end_date:
        url_TW_k,url_TW_v=TwseIndex.get_TWindex_url(start_date)
        jsondata_TW_k=get_json_by_url(url_TW_k)
        time.sleep(1)
        jsondata_TW_v=get_json_by_url(url_TW_v)
        TAIEX_data=TwseIndex.clean_index_data(jsondata_TW_k, jsondata_TW_v)
        if TAIEX_data:
            StockModel.save_TAIEX_prices(TAIEX_data)
            print(f"[{start_date.strftime('%Y-%m')}] 儲存完成。")
        else:
            print(f"[{start_date.strftime('%Y-%m')}] 無資料或抓取異常。")

        start_date = start_date.replace(day=1) - timedelta(days=1)
        sleep_time = random.uniform(12, 20) 
        time.sleep(sleep_time)

# start = date(2021, 1, 1)
# end = date(2020, 1, 1)
# get_TwseIndex_data(start, end) # 上市大盤進度

def get_TpexStock_data(start_date, end_date):  # 資料進度 2026, 1, 1
    number_data = set(StockModel.get_all_stock_numbers())
    while start_date >= end_date:
        if start_date.weekday() >= 5:
            start_date -= timedelta(days=1)
            continue
        jsondata=TpexStock.get_tpex_data(start_date)
        stock_data=TpexStock.clean_Tpexstock_data(jsondata, number_data, start_date)
        if stock_data:          
            StockModel.save_stock_prices(stock_data)
            print(f"[{start_date}] 儲存完成。")
        else:
            print(f"[{start_date}] 無資料 (可能是休市)。")

        start_date -= timedelta(days=1)
        sleep_time = random.uniform(5, 12) 
        time.sleep(sleep_time)

# start = date(2026, 2, 24)
# end = date(2026, 2, 4)
# get_TpexStock_data(start, end) # 上櫃個股進度