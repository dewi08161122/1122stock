from fastapi import APIRouter
from models.search_model import SearchModel
from datetime import timedelta, date

router = APIRouter()

@router.get("/api/hotstock/value")
def gethotstock():
    try:
        trade_date = date.today()
        data = SearchModel.get_trade_value_ranking(trade_date)
        retry_limit = 10
        while not data and retry_limit > 0:
            trade_date -= timedelta(days=1)
            retry_limit -= 1
            if trade_date.weekday() >= 5:
                continue
            data = SearchModel.get_trade_value_ranking(trade_date)
        return data
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}