from services.twse_stock_service import TwseStock
from services.twse_index_service import TwseIndex
from services.tpex_stock_service import TpexStock
from services.tpex_index_service import TpexIndex
from models.save_stock_model import StockModel
from infrastructure.network import get_json_by_url
from infrastructure.redis import cleanup_after_crawl
import time, random
from datetime import timedelta, date

def get_TwseStock_data(start_date, end_date): 
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

def get_TwseIndex_data(start_date, end_date):  
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

def get_TpexStock_data(start_date, end_date):  
    number_data = set(StockModel.get_all_stock_numbers())
    while start_date >= end_date:
        if start_date.weekday() >= 5:
            start_date -= timedelta(days=1)
            continue
        jsondata=TpexStock.get_Tpexstock_data(start_date)
        stock_data=TpexStock.clean_Tpexstock_data(jsondata, number_data, start_date)
        date_str = start_date.strftime("%Y-%m-%d")
        Tpex_value=TpexIndex.clean_TpexIndex_valuedata(jsondata)
        if stock_data :          
            StockModel.save_stock_prices(stock_data)
        if Tpex_value:
            StockModel.save_TPEX_value(Tpex_value, date_str)
        if stock_data or Tpex_value:
            print(f"[{start_date}] 儲存完成。")
        else:
            print(f"[{start_date}] 無資料 (可能是休市)。")

        start_date -= timedelta(days=1)
        sleep_time = random.uniform(5, 12) 
        time.sleep(sleep_time)

def get_TpexIndex_data(start_date, end_date): 
    while start_date >= end_date:
        jsondata=TpexIndex.get_TpexIndex_data(start_date)
        TPEX_data=TpexIndex.clean_TpexIndex_data_without_value(jsondata)
        if TPEX_data:
            StockModel.save_TPEX_prices(TPEX_data)
            print(f"[{start_date.strftime('%Y-%m')}] 儲存完成。")
        else:
            print(f"[{start_date.strftime('%Y-%m')}] 無資料或抓取異常。")

        start_date = start_date.replace(day=1) - timedelta(days=1)
        sleep_time = random.uniform(12, 20) 
        time.sleep(sleep_time)


def get_today():
    try:
        start = date.today()
        end = date.today()
        get_TwseIndex_data(start, end)
        get_TpexIndex_data(start, end)
        get_TwseStock_data(start, end)
        get_TpexStock_data(start, end)
        StockModel.all_kline_to_week_month(start.strftime('%Y-%m-%d'))
        cleanup_after_crawl()
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")
    finally:
        print("--- 每日更新程序結束 ---", flush=True)

get_today()

