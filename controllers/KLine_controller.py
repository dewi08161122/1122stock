from fastapi import APIRouter, Query
from models.KLine_model import KLineModel

router = APIRouter()
    
@router.get("/api/stock/{number}")
def getStockKLine(number: str, offset: int = 0, period: str = Query("day", enum=["day", "week", "month"])):
    try:
        if number == "TAIEX":
            if period == "week":
                KLine = KLineModel.get_TAIEX_KLine_week()
            elif period == "month":
                KLine = KLineModel.get_TAIEX_KLine_month()
            else:
                KLine = KLineModel.get_TAIEX_KLine(offset)
        elif number == "TPEX":
            if period == "week":
                KLine = KLineModel.get_TPEX_KLine_week()
            elif period == "month":
                KLine = KLineModel.get_TPEX_KLine_month()
            else:
                KLine = KLineModel.get_TPEX_KLine(offset)
        else:
            if period == "week":
                KLine = KLineModel.get_stock_KLine_week(number)
            elif period == "month":
                KLine = KLineModel.get_stock_KLine_month(number)
            else:
                KLine = KLineModel.get_stock_KLine(number, offset)
        if KLine is None: 
            return {"error": True, "message": "無此股票代碼或資料不存在"}
        return KLine
    except Exception as e:
        print(e)
        return{"error":True,"message":"伺服器內部錯誤"}